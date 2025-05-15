import contextlib
import dataclasses

from localsend import callbacks, config, info, tasks, upload
from localsend.lib import ssl


@dataclasses.dataclass
class App:
    uploader: upload.Uploader
    callbacks: callbacks.Callbacks


@contextlib.asynccontextmanager
async def create_app(config: config.Config):
    callbacks_ = callbacks.Callbacks()
    ssl_ctx = ssl.Context.create(config.ssl) if config.ssl != 'disabled' else None
    info_ctx = info.Context.create(config.info, ssl_ctx)
    tasks_ctx = await tasks.Context.create(
        config.http_server, config.multicast, info_ctx, callbacks_
    )
    try:
        async with upload.Uploader.create(config.upload, info_ctx) as uploader:
            yield App(uploader, callbacks_)
    finally:
        await tasks_ctx.cancel()
