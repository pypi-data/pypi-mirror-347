import asyncio
import operator
from collections.abc import Awaitable, Callable
from typing import TypeVar
from unittest import mock

import pytest

from sloths import Stream
from sloths.ext.asyncio import AsyncStream

pytestmark = [pytest.mark.asyncio]

T = TypeVar("T")


# Tests extracted from the doctests as they are otherwise cumbersome to write
# with asyncio.


def add2(x: int) -> int:
    return x * 2


async def a_add2(x: int) -> int:
    await asyncio.sleep(0.001)
    return x * 2


def is_even(x: int) -> bool:
    return x % 2 == 0


async def a_is_even(x: int) -> bool:
    await asyncio.sleep(0.001)
    return x % 2 == 0


async def a_add(x: int, y: int) -> int:
    return x + y


@pytest.mark.parametrize(
    ("expected", "factory"),
    [
        (
            [0, 1, 2, 0, 1, 2, 0, 1, 2],
            lambda: AsyncStream.range(3).chain(
                AsyncStream.range(3),
                AsyncStream.range(3),
            ),
        ),
        ([0, 1, 2], lambda: AsyncStream.range(3).chain()),
        (
            [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10)],
            lambda: AsyncStream.range(5, 11).enumerate(),
        ),
        ([0, 2, 4, 6], lambda: AsyncStream.range(4).map(add2)),
        ([0, 2, 4, 6], lambda: AsyncStream.range(4).amap(a_add2)),
        ([0, 2], lambda: AsyncStream.range(4).filter(is_even)),
        ([1, 2, 3], lambda: AsyncStream.range(4).filter()),
        ([0, 2], lambda: AsyncStream.range(4).afilter(a_is_even)),
        (
            [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10,)],
            lambda: AsyncStream.range(11).batch(2),
        ),
        ([], lambda: AsyncStream.range(2).skip(4)),
        ([2, 3], lambda: AsyncStream.range(4).skip(2)),
    ],
)
async def test_async_stream_simple_cases(
    expected: list[T],
    factory: Callable[[], AsyncStream[T]],
) -> None:
    assert expected == await factory().collect()


@pytest.mark.parametrize(
    ("expected", "err", "factory"),
    [
        (0, None, lambda: AsyncStream.range(0).count()),
        (10, None, lambda: AsyncStream.range(10).count()),
        (0, None, lambda: AsyncStream.range(10).nth(0)),
        (2, None, lambda: AsyncStream.range(10).nth(2)),
        (None, None, lambda: AsyncStream.range(10).nth(20, default=None)),
        (None, (IndexError, "20"), lambda: AsyncStream.range(10).nth(20)),
        (3, None, lambda: AsyncStream.range(10).find(lambda x: x == 3)),
        (None, None, lambda: AsyncStream.range(10).find(lambda x: x == -2)),
        (1, None, lambda: AsyncStream.range(10).find()),
        (4, None, lambda: AsyncStream.range(10).skip(3).afind(a_is_even)),
        (45, None, lambda: AsyncStream.range(10).fold(operator.add, 0)),
        (55, None, lambda: AsyncStream.range(10).fold(operator.add, 10)),
        (45, None, lambda: AsyncStream.range(10).afold(a_add, 0)),
        (55, None, lambda: AsyncStream.range(10).afold(a_add, 10)),
    ],
)
async def test_async_stream_simple_reducers(
    expected: T | None,
    err: tuple[type[Exception], "str"] | None,
    factory: Callable[[], Awaitable[T]],
) -> None:
    if err is not None:
        ecls, ematch = err
        with pytest.raises(ecls, match=ematch):
            await factory()
    else:
        assert expected == await factory()


async def test_take():
    s = AsyncStream.range(10)
    assert [0, 1, 2, 3] == await s.take(4).collect()
    assert 4 == await anext(s)

    assert [0, 1, 2, 3] == await AsyncStream.range(4).take(
        10,
    ).collect()


async def test_try_map():
    def no_2(x: int) -> int:
        if x == 2:
            raise ValueError(2)
        return x

    with pytest.raises(ValueError, match="2"):
        await AsyncStream.range(10).map(no_2).collect()

    assert [0, 1, 3, 4, 5, 6, 7, 8, 9] == await AsyncStream.range(10).try_map(
        no_2,
        (ValueError,),
    ).collect()

    cb = mock.MagicMock()
    await AsyncStream.range(10).try_map(no_2, (ValueError,), cb=cb).collect()
    cb.assert_called_once_with(mock.ANY, 2)


async def test_atry_map():
    async def no_2(x: int) -> int:
        await asyncio.sleep(0.001)
        if x == 2:
            raise ValueError(2)
        return x

    with pytest.raises(ValueError, match="2"):
        await AsyncStream.range(10).amap(no_2).collect()

    assert [0, 1, 3, 4, 5, 6, 7, 8, 9] == await AsyncStream.range(10).atry_map(
        no_2,
        (ValueError,),
    ).collect()

    cb = mock.MagicMock()
    await AsyncStream.range(10).atry_map(no_2, (ValueError,), cb=cb).collect()
    cb.assert_called_once()
    assert isinstance(cb.call_args[0][0], ValueError)
    assert cb.call_args[0][1] == 2


async def test_try():
    def no_2(x: int) -> int:
        if x == 2:
            raise ValueError(2)
        return x

    with pytest.raises(ValueError, match="2"):
        await AsyncStream.range(10).map(no_2).collect()

    assert [0, 1] == await AsyncStream.range(10).map(no_2).try_(
        (ValueError,),
    ).collect()

    cb = mock.MagicMock()
    await AsyncStream.range(10).map(no_2).try_((ValueError,), cb=cb).collect()
    cb.assert_called_once()
    assert isinstance(cb.call_args[0][0], ValueError)


async def test_to_async():
    assert [0, 2, 4, 6, 8] == await Stream(range(10)).to_async().afilter(
        a_is_even,
    ).collect()
