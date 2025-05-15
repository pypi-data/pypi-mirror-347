import asyncio
import contextlib
import dataclasses
import datetime
import mimetypes
import typing
import uuid

import httpx
import pydantic

from localsend import info
from localsend.lib import dto, protocol, util


class Config(pydantic.BaseModel):
    max_connections: int | None = None
    check_device: bool = True
    default_mime_type: str = 'application/octet-stream'
    batch_size: pydantic.ByteSize = pydantic.ByteSize(4096)


class AsyncReadableIO(typing.Protocol):
    async def read(self, n: int = -1, /) -> bytes: ...


@dataclasses.dataclass
class File:
    name: str
    size: pydantic.ByteSize
    input: typing.Callable[[], typing.AsyncContextManager[AsyncReadableIO]]
    mime_type: str | None = None
    sha256: str | None = None
    preview: str | None = None
    modified: datetime.datetime | None = None
    accessed: datetime.datetime | None = None


def get_mime_type(file: File, config: Config):
    if file.mime_type is not None:
        return file.mime_type

    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type is not None:
        return mime_type

    return config.default_mime_type


@dataclasses.dataclass
class Uploader:
    config: Config
    info_ctx: info.Context
    client: protocol.Client

    @staticmethod
    @contextlib.asynccontextmanager
    async def create(config: Config, info_ctx: info.Context):
        async with httpx.AsyncClient(
            verify=False, limits=httpx.Limits(max_connections=config.max_connections)
        ) as http_client:
            yield Uploader(config, info_ctx, protocol.Client(http_client))

    async def _upload_file(
        self,
        file: File,
        file_id: str,
        device: protocol.Device,
        prepare_response: dto.PrepareUploadResponse,
    ):
        async with file.input() as f:

            async def reader():
                while True:
                    chunk = await f.read(self.config.batch_size)
                    if len(chunk) == 0:
                        break

                    yield chunk

            await self.client.call_upload(
                device,
                dto.UploadParams(
                    sessionId=prepare_response.sessionId,
                    fileId=file_id,
                    token=prepare_response.files[file_id],
                ),
                reader(),
            )

    async def upload(self, files: list[File], device: protocol.Device):
        if self.config.check_device:
            device_info = await self.client.call_info_v1(device)
            if device_info.fingerprint != device.info.fingerprint:
                util.LOGGER.info('Device info are not matching, skipping upload')
                return

        id_file_map = {str(uuid.uuid4()): file for file in files}

        prepare_response = await self.client.call_prepare_upload(
            device,
            dto.PrepareUploadRequest(
                info=self.info_ctx.to_dto(),
                files={
                    id: dto.File(
                        id=id,
                        fileName=file.name,
                        size=file.size,
                        fileType=get_mime_type(file, self.config),
                        sha256=file.sha256,
                        preview=file.preview,
                        metadata=dto.FileMetadata(modified=file.modified, accessed=file.accessed),
                    )
                    for id, file in id_file_map.items()
                },
            ),
        )

        try:
            await asyncio.gather(
                *(
                    self._upload_file(id_file_map[file_id], file_id, device, prepare_response)
                    for file_id in prepare_response.files
                )
            )
        except Exception:
            await self.client.call_cancel(
                device, dto.CancelParams(sessionId=prepare_response.sessionId)
            )
