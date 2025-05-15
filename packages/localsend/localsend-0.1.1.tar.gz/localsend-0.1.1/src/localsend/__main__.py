import asyncio
import pathlib

import aiofiles
import pydantic

import localsend
from localsend.lib import datadir, util

with util.add_exception_note('To use the localsend command, please install localsend[cli]'):
    import cyclopts
    import slcfg


def read_config():
    return slcfg.read_config(
        localsend.Config,
        [
            slcfg.toml_file_layer(datadir.get_config_dir() / 'config.toml', optional=True),
            slcfg.env_layer('LOCALSEND_', '__'),
        ],
    )


APP = cyclopts.App()


@APP.command
async def receive():
    async with localsend.create_app(config=read_config()) as app:

        async def accept(_device: localsend.Device, file: localsend.FileDto):
            path = datadir.get_downloads_dir() / file.fileName
            path.parent.mkdir(parents=True, exist_ok=True)
            return aiofiles.open(path, mode='wb')

        app.callbacks.accept = accept
        while True:
            await asyncio.sleep(60)


@APP.command
async def send(path: pathlib.Path):
    async with localsend.create_app(config=read_config()) as app:

        async def new_device(device: localsend.Device):
            await app.uploader.upload(
                [
                    localsend.File(
                        path.name,
                        pydantic.ByteSize(path.stat().st_size),
                        input=lambda: aiofiles.open(path, mode='rb'),
                    )
                ],
                device,
            )

        app.callbacks.new_device = new_device
        while True:
            await asyncio.sleep(60)
