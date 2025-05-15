import contextlib
import typing


@contextlib.contextmanager
def optional_context[T](
    ctx: typing.ContextManager[T] | None,
) -> typing.Iterator[T | None]:
    if ctx is None:
        yield None
        return

    with ctx as t:
        yield t


@contextlib.asynccontextmanager
async def async_context[T](
    ctx: typing.ContextManager[T],
) -> typing.AsyncIterator[T]:
    with ctx as t:
        yield t
