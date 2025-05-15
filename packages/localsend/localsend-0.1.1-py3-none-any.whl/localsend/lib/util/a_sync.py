import asyncio
import contextlib
import functools
import threading
import typing


async def wait_sync(target: typing.Callable[[threading.Event], None]):
    cancel_sync = threading.Event()
    future = asyncio.get_event_loop().run_in_executor(None, lambda: target(cancel_sync))
    try:
        await future
    except asyncio.CancelledError:
        cancel_sync.set()


def create_task[T](awaitable: typing.Awaitable[T]):
    if asyncio.iscoroutine(awaitable):
        coroutine = awaitable
    else:

        async def coroutine_func():
            return await awaitable

        coroutine = coroutine_func()

    return asyncio.create_task(coroutine)


class BackgroundTaskManager:
    def __init__(self):
        self.next_task_id = 0
        self.tasks: dict[int, asyncio.Task[None]] = {}

    def clean(self):
        for id, task in list(self.tasks.items()):
            if task.done():
                del self.tasks[id]
                with contextlib.suppress(asyncio.CancelledError):
                    task.result()

    def add(self, awaitable: typing.Awaitable[typing.Any]):
        self.tasks[self.next_task_id] = create_task(awaitable)
        self.next_task_id += 1
        self.clean()


def make_async[**P, R](callable: typing.Callable[P, R]):
    @functools.wraps(callable)
    async def wrapper(*args: P.args, **kwargs: P.kwargs):
        return callable(*args, **kwargs)

    return wrapper
