import asyncio
import dataclasses

from localsend import callbacks, info
from localsend.tasks import http_server, multicast


async def create_http_serve_task(
    config: http_server.Config, info_ctx: info.Context, callbacks: callbacks.Callbacks
):
    ready = asyncio.Event()
    task = asyncio.create_task(http_server.serve(config, info_ctx, ready, callbacks))
    await ready.wait()
    return task


def create_multicast_receive_task(
    config: multicast.Config, info_ctx: info.Context, callbacks: callbacks.Callbacks
):
    return asyncio.create_task(multicast.receive(callbacks, config, info_ctx))


def create_multicast_send_task(config: multicast.Config, info_ctx: info.Context):
    return asyncio.create_task(multicast.send(config, info_ctx))


@dataclasses.dataclass
class Context:
    http_serve: asyncio.Task[None]
    multicast_receive: asyncio.Task[None]
    multicast_send: asyncio.Task[None]

    @staticmethod
    async def create(
        http_sever_config: http_server.Config,
        multicast_config: multicast.Config,
        info_ctx: info.Context,
        callbacks: callbacks.Callbacks,
    ):
        http_serve = await create_http_serve_task(http_sever_config, info_ctx, callbacks)
        multicast_receive = create_multicast_receive_task(multicast_config, info_ctx, callbacks)
        multicast_send = create_multicast_send_task(multicast_config, info_ctx)

        return Context(
            http_serve=http_serve,
            multicast_receive=multicast_receive,
            multicast_send=multicast_send,
        )

    async def cancel(self):
        self.http_serve.cancel()
        self.multicast_receive.cancel()
        self.multicast_send.cancel()
        await asyncio.gather(self.http_serve, self.multicast_receive, self.multicast_send)
