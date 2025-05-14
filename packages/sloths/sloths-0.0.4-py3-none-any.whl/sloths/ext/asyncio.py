"""
asyncio native stream class.
"""

from __future__ import annotations

import functools
import inspect
from collections.abc import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterable,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    Literal,
    ParamSpec,
    SupportsIndex,
    TypeAlias,
    TypeVar,
    cast,
    overload,
)

from sloths._utils import UNSET

if TYPE_CHECKING:
    from collections.abc import Awaitable, Iterable

T = TypeVar("T")
U = TypeVar("U")

P = ParamSpec("P")


AsyncTransform: TypeAlias = Callable[
    Concatenate[AsyncIterable[T], P],
    AsyncIterable[U],
]


class AsyncStream(Generic[T], AsyncIterable[T]):
    """
    Async version of :class:`sloths.Stream` but async iterators.

    It works essentially the same and expose the same interface but in an
    async/await compatible manner.

    Some functions which take callbacks such as :meth:`map` also have
    prefixed async equivalent :meth:`amap` which take an async callback
    instead.
    """

    def __init__(self, source: AsyncIterable[T]) -> None:
        self._source = source

    @classmethod
    def range(
        cls: type[AsyncStream[int]],
        *args: SupportsIndex,
    ) -> AsyncStream[int]:
        """
        Create a simple async stream over ``range()``.
        """
        return AsyncStream(make_async(range(*args)))

    @classmethod
    def from_iterable(cls, source: Iterable[T]) -> AsyncStream[T]:
        """
        Wrap a sync iterable.
        """
        return cls(make_async(source))

    @functools.cached_property
    def _iter(self) -> AsyncIterator[T]:
        return aiter(self._source)

    async def __aiter__(self) -> AsyncIterator[T]:
        async for x in self._iter:
            yield x

    async def __anext__(self) -> T:
        return await anext(self._iter)

    def __repr__(self) -> str:
        return f"AsyncStream<{self._source!r}>"

    def chain(self, *others: AsyncIterable[T]) -> AsyncStream[T]:
        """
        Chain one or more async iterables to the current ones.

        .. seealso:: :meth:`sloths.Stream.chain`
        """

        async def _chained():
            for it in (self, *others):
                async for x in it:
                    yield x

        return AsyncStream(_chained())

    def pipe(
        self,
        fn: AsyncTransform[T, P, U],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> AsyncPipe[T, P, U]:
        """
        Chain a transform to a stream and return the resulting stream.

        .. seealso:: :meth:`sloths.Stream.pipe`

        Transforms are the core composability primitive and are simply callables
        which take an iterable and return another iterable. Usually these are
        lazy generators.

        >>> import asyncio

        >>> async def to_str(iterable: AsyncIterable[int]) -> \
            AsyncIterable[str]:
        ...     async for x in iterable:
        ...         yield str(x)
        ...
        >>> asyncio.run(AsyncStream.range(10).pipe(to_str).collect())
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        Transforms can also decide to short-circuit or selectively yield for
        control-flow:

        >>> async def to_str_if_odd(iterable: AsyncIterable[int]) -> \
            AsyncIterable[str]:
        ...     async for x in iterable:
        ...         if x % 2:
        ...             yield str(x)
        ...
        >>> asyncio.run(AsyncStream.range(10).pipe(to_str_if_odd).collect())
        ['1', '3', '5', '7', '9']

        And all the same properties as the sync version.

        .. warning::
            When writing transforms be careful not to accidentally consume the
            iterable as this would negate much of the benefit of chaining
            generators in the first place.
        """
        return AsyncPipe(self, fn, fn.__name__, *args, **kwargs)

    # Chained operations

    def inspect(self: AsyncStream[T], cb: Callable[[T], Any]) -> AsyncStream[T]:
        """
        Execute a function on each element without modifying it.

        .. seealso:: :meth:`sloths.Stream.inspect`

        This is mostly useful for debugging but could be used as the base for
        monitoring and metrics or any other side-effects.
        """

        async def inspect(gen: AsyncIterable[T]) -> AsyncIterable[T]:
            async for x in gen:
                cb(x)
                yield x

        return AsyncPipe(
            self,
            inspect,
            name=f"inspect<{getattr(cb, '__name__', None) or repr(cb)}>",
        )

    def enumerate(self: AsyncStream[T]) -> AsyncStream[tuple[int, T]]:
        """
        Python's ``enumerate`` as a transform.

        .. seealso:: :meth:`sloths.Stream.enumerate`
        """

        async def _enumerate(
            gen: AsyncIterable[T],
        ) -> AsyncIterable[tuple[int, T]]:
            i = 0
            async for x in gen:
                yield i, x
                i += 1

        return self.pipe(_enumerate)

    def map(self, fn: Callable[[T], U]) -> AsyncStream[U]:
        """
        Run a synchronous element-wise transform over the stream.

        .. seealso:: :meth:`sloths.Stream.map`
        """

        async def _map(gen: AsyncIterable[T]) -> AsyncIterable[U]:
            async for x in gen:
                yield fn(x)

        return AsyncPipe(self, _map, name=f"map({fn})")

    def try_map(
        self,
        fn: Callable[[T], U],
        exc_cls: tuple[type[Exception], ...] = (Exception,),
        *,
        cb: Callable[[Exception, T], None] | None = None,
    ) -> AsyncStream[U]:
        """
        Run a synchronous element-wise transform over the stream and discard errors.

        .. seealso:: :meth:`sloths.Stream.try_map`
        """  # noqa: E501

        async def _map_except(gen: AsyncIterable[T]) -> AsyncIterable[U]:
            async for x in gen:
                try:
                    y = fn(x)
                except exc_cls as e:
                    if cb:
                        cb(e, x)
                    continue
                yield y

        return AsyncPipe(
            self,
            _map_except,
            name=f"try_map({fn}, {exc_cls}, {cb})",
        )

    def amap(self, fn: Callable[[T], Awaitable[U]]) -> AsyncStream[U]:
        """
        Run an asynchronous element-wise transform over the stream.

        This is equivalent to ``AsyncStream(...).map(...).flatten()``.
        """

        async def _map(gen: AsyncIterable[T]) -> AsyncIterable[U]:
            async for x in gen:
                yield await fn(x)

        return AsyncPipe(self, _map, name=f"map({fn})")

    def atry_map(
        self,
        fn: Callable[[T], Awaitable[U]],
        exc_cls: tuple[type[Exception], ...] = (Exception,),
        *,
        cb: Callable[[Exception, T], None] | None = None,
    ) -> AsyncStream[U]:
        """
        Run an asynchronous element-wise transform over the stream discard errors.
        """  # noqa: E501

        async def _map_except(gen: AsyncIterable[T]) -> AsyncIterable[U]:
            async for x in gen:
                try:
                    y = await fn(x)
                except exc_cls as e:
                    if cb:
                        cb(e, x)
                    continue
                yield y

        return AsyncPipe(
            self,
            _map_except,
            name=f"try_map({fn}, {exc_cls}, {cb})",
        )

    def try_(
        self,
        exc_cls: tuple[type[Exception], ...] = (Exception,),
        *,
        cb: Callable[[Exception], None] | None = None,
    ) -> AsyncStream[T]:
        """
        Stop on the first exception and discard it.

        .. seealso:: :meth:`sloths.Stream.try_`

        This is more generic than :meth:`try_map` and will catch error that
        happened when calling ``next()`` on the upstream transform but will stop
        iteration on the first exception.
        """

        async def _try(gen: AsyncIterable[T]) -> AsyncIterable[T]:
            it = aiter(gen)
            while True:
                try:
                    yield await anext(it)
                except StopAsyncIteration:  # noqa: PERF203
                    return
                except exc_cls as e:
                    if cb:
                        cb(e)
                    return

        return AsyncPipe(
            self,
            _try,
            name=f"stop_on_exception({exc_cls}, {cb})",
        )

    def batch(self, by: int) -> AsyncStream[tuple[T, ...]]:
        """
        Buffer the stream and provide groups to downstream consumers.

        .. seealso:: :meth:`sloths.Stream.batch`

        .. warning::
            This partially unwinds the stream and will increase memory usage.
            Only buffer to amounts you're comfortable holding in memory at once.
        """
        return AsyncPipe(self, _batch, name=f"batch(by={by})", by=by)

    def flatten(
        self: AsyncStream[AsyncIterable[U]]
        | AsyncStream[Iterable[U]]
        | AsyncStream[Awaitable[U]],
    ) -> AsyncStream[U]:
        """
        Flatten iterators into their elements.

        This will flatten iterables, async iterables and awaitable, so it has
        the same utility as :meth:`sloths.Stream.flatten`:

        >>> import asyncio

        >>> asyncio.run(AsyncStream.range(11).batch(by=2).flatten().collect())
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        But can also be used to flatten async results (this trivial case is
        equivalent to calling :meth:`amap`):

        >>> async def aadd_2(x):
        ...     await asyncio.sleep(0.001)
        ...     return x + 2
        >>> asyncio.run(AsyncStream.range(11).map(aadd_2).flatten().collect())
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        Or async iterables:

        >>> async def apair(x):
        ...     await asyncio.sleep(0.001)
        ...     for _ in range(2):
        ...         yield x
        >>> asyncio.run(AsyncStream.range(5).map(apair).flatten().collect())
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        """
        # I am pretty sure this is correct in practice but the type inference is
        # unhappy. Need to revisit.
        return AsyncPipe(self, _flatten, name="flatten")  # type: ignore

    def filter(
        self,
        predicate: Callable[[T], bool] | None = None,
    ) -> AsyncStream[T]:
        """
        Filter elements by running them through a predicate function.

        .. seealso:: :meth:`sloths.Stream.filter`

        """

        async def _filter(gen: AsyncIterable[T]) -> AsyncIterable[T]:
            if predicate:
                async for x in gen:
                    if predicate(x):
                        yield x
            else:
                async for x in gen:
                    if x:
                        yield x

        return AsyncPipe(self, _filter, name=f"filter({predicate})")

    def afilter(
        self,
        predicate: Callable[[T], Awaitable[bool]],
    ) -> AsyncStream[T]:
        """
        Filter elements by running them through an asynchronous  predicate.
        """

        async def _filter(gen: AsyncIterable[T]) -> AsyncIterable[T]:
            async for x in gen:
                if await predicate(x):
                    yield x

        return AsyncPipe(self, _filter, name=f"filter({predicate})")

    def take(self, count: int) -> AsyncStream[T]:
        """
        Take up to ``count`` element from the stream and interrupt.

        .. seealso:: :meth:`sloths.Stream.take`

        Upstream generators will not be polled once we've reached the requested
        number of elements so the source can be consumed to its end separately.
        """
        return AsyncPipe(self, _take, name=f"take({count})", n=count)

    def skip(self, count: int) -> AsyncStream[T]:
        """
        Skip over ``count`` element from the iterator.

        .. seealso:: :meth:`sloths.Stream.skip`
        """
        return AsyncPipe(self, _skip, name=f"skip({count})", n=count)

    def take_while(
        self,
        predicate: Callable[[T], bool] | None = None,
    ) -> AsyncStream[T]:
        """
        Consume element from the stream until the predicate returns ``False``.

        .. seealso:: :meth:`sloths.Stream.take_while`
        """
        return AsyncPipe(
            self,
            _take_while,
            name=f"take_while({predicate})",
            predicate=predicate,
        )

    def skip_while(
        self,
        predicate: Callable[[T], bool] | None = None,
    ) -> AsyncStream[T]:
        """
        Skip elements until the predicate returns ``True``.

        .. seealso:: :meth:`sloths.Stream.skip_while`
        """
        return AsyncPipe(
            self,
            _skip_while,
            name=f"drop_while({predicate})",
            predicate=predicate,
        )

    # Reducer / consuming methods

    async def consume(self):
        """
        Consume the stream but discard the results.

        This is useful for infinite pipelines or processing pipelines where the
        results are not important.
        """
        async for _ in self:
            pass

    @overload
    async def collect(self) -> list[T]: ...

    @overload
    async def collect(
        self,
        collector: Callable[[AsyncIterable[T]], U],
    ) -> U: ...

    async def collect(
        self,
        collector: Callable[[AsyncIterable[T]], U] | None = None,
    ) -> U | list[T]:
        """
        Collect the iterator.

        By default this collects into a list but custom collectors are also
        supported as long as they accept async iterables as input.
        """
        if collector is None:
            return [x async for x in self]
        return collector(x async for x in self)

    async def count(self) -> int:
        """
        Return the length of the stream after consuming it.

        ``__alen__`` would implicitly consume the stream in various places so is
        unsafe to add.
        """
        s = 0
        async for _ in self:
            s += 1
        return s

    @overload
    async def nth(self, nth: int) -> T: ...

    @overload
    async def nth(self, nth: int, *, default: T) -> T: ...

    @overload
    async def nth(self, nth: int, *, default: U) -> T | U: ...

    async def nth(
        self,
        nth: int,
        *,
        default: U | Literal[UNSET.U] = UNSET.U,
    ) -> T | U:
        """
        Return the ``nth`` value.

        .. seealso:: :meth:`sloths.Stream.nth`

        Raises ``IndexError`` if the stream isn't long enough and a default
        value is not provided.
        """
        await self.take(nth).consume()
        if default is not UNSET.U:
            return await anext(self, default)
        try:
            return await anext(self)
        except StopAsyncIteration:
            raise IndexError(nth) from None

    async def find(
        self,
        predicate: Callable[[T], bool] | None = None,
    ) -> T | None:
        """
        Find the first elements that satisfies a predicate.

        .. seealso:: :meth:`sloths.Stream.find`

        This short-cirtcuits so it won't consume the source iterator past the
        target element:
        """
        return await anext(self.filter(predicate), None)

    async def afind(
        self,
        predicate: Callable[[T], Awaitable[bool]],
    ) -> T | None:
        """
        Find the first elements that satisfies an asynchronous predicate.

        This short-cirtcuits so it won't consume the source iterator past the
        target element:
        """
        return await anext(self.afilter(predicate), None)

    async def fold(self, fn: Callable[[U, T], U], acc: U) -> U:
        """
        Fold every element into an accumulator function.

        .. seealso:: :meth:`sloths.Stream.fold`
        """
        cur = acc
        async for x in self:
            cur = fn(cur, x)
        return cur

    async def afold(self, fn: Callable[[U, T], Awaitable[U]], acc: U) -> U:
        """
        Fold every element into an asynchronous accumulator function.
        """
        cur = acc
        async for x in self:
            cur = await fn(cur, x)
        return cur


class AsyncPipe(Generic[T, P, U], AsyncStream[U]):
    """
    A stream representing a source stream passed through a transform function.

    This should not be interacted with directly.

    .. seealso::
        :meth:`Stream.pipe`
    """

    def __init__(
        self,
        source: AsyncIterable[T],
        fn: AsyncTransform[T, P, U],
        name: str | None = None,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        self._inner = source
        self._transform = fn
        self._name = name
        self._iterator: AsyncIterator[U] | None = None
        self._args = args
        self._kwargs = kwargs

    @functools.cached_property
    def _iter(self) -> AsyncIterator[U]:
        return aiter(
            self._transform(
                aiter(self._inner),
                *self._args,
                **self._kwargs,
            ),
        )

    def __str__(self) -> str:
        name = self._name or repr(self._transform)
        return f"{self._inner} | {name}({self._args}, {self._kwargs})"

    def __repr__(self) -> str:
        return f"AsyncPipe<{self!s}>"


#  Async iterator utils


async def make_async(it: Iterable[T]) -> AsyncIterable[T]:
    """
    Wrap a synchronous iterator in an asynchronous one.
    """
    for x in iter(it):
        yield x


async def _batch(it: AsyncIterable[T], by: int) -> AsyncIterable[tuple[T, ...]]:
    """
    Chunk an iterable into tuples of a given size.
    """
    iterator = aiter(it)
    _batch: list[T] = []
    try:
        while True:
            for _ in range(by):
                _batch.append(await anext(iterator))  # noqa: PERF401
            yield tuple(_batch)
            del _batch[:]
    except StopAsyncIteration:
        if _batch:
            yield tuple(_batch)


# @overload
# def _flatten(
#     gen: AsyncIterable[AsyncIterable[U]],
# ) -> AsyncIterable[U]: ...


# @overload
# def _flatten(
#     gen: AsyncIterable[Iterable[U]],
# ) -> AsyncIterable[U]: ...


# @overload
# def _flatten(
#     gen: AsyncIterable[Awaitable[U]],
# ) -> AsyncIterable[U]: ...


async def _flatten(
    gen: AsyncIterable[AsyncIterable[U]]
    | AsyncIterable[Iterable[U]]
    | AsyncIterable[Awaitable[U]],
) -> AsyncIterable[U]:
    """
    Flatten an async iterator of awaitables, iterables, or async iterables.
    """
    it = aiter(gen)
    try:
        first = await anext(it)
    except StopAsyncIteration:
        return

    if inspect.isawaitable(first):
        yield await first
        async for x in cast("AsyncIterator[Awaitable[U]]", it):
            yield await x
    elif isinstance(first, (AsyncIterable, AsyncIterator)):
        async for y in first:
            yield y
        async for x in cast("AsyncIterator[AsyncIterable[U]]", it):
            async for y in x:
                yield y
    else:
        for y in first:
            yield y
        async for x in cast("AsyncIterator[Iterable[U]]", it):
            for y in x:
                yield y


async def _take(gen: AsyncIterable[T], *, n: int) -> AsyncIterable[T]:
    it = aiter(gen)
    try:
        for _ in range(n):
            yield await anext(it)
    except StopAsyncIteration:
        return


async def _skip(gen: AsyncIterable[T], *, n: int) -> AsyncIterable[T]:
    it = aiter(gen)
    try:
        for _ in range(n):
            await anext(it)
    except StopAsyncIteration:
        return

    async for x in it:
        yield x


async def _take_while(
    gen: AsyncIterable[T],
    *,
    predicate: Callable[[T], bool] | None = None,
) -> AsyncIterable[T]:
    it = aiter(gen)
    if predicate:
        async for x in it:
            if predicate(x):
                yield x
            else:
                return
    else:
        async for x in it:
            if x:
                yield x
            else:
                return


async def _skip_while(
    gen: AsyncIterable[T],
    *,
    predicate: Callable[[T], bool] | None = None,
) -> AsyncIterable[T]:
    it = aiter(gen)
    if predicate:
        async for x in it:
            if not predicate(x):
                break
    else:
        async for x in it:
            if not x:
                break

    async for x in it:
        yield x
