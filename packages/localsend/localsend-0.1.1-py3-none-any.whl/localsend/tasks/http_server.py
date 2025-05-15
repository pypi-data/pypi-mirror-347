import asyncio
import contextlib
import dataclasses
import ipaddress
import os
import typing
import uuid

import pydantic
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from localsend import callbacks, info
from localsend.lib import dto, protocol, util


class Config(pydantic.BaseModel):
    host: pydantic.IPvAnyAddress = ipaddress.IPv4Address('0.0.0.0')
    workers: int | None = None
    dev_mode: bool = False


@dataclasses.dataclass
class Upload:
    id: str
    session_id: str
    file: dto.File
    output: callbacks.AcceptResult


Sessions: typing.TypeAlias = dict[str, dict[str, Upload]]


@dataclasses.dataclass
class State:
    config: Config
    info_ctx: info.Context
    callbacks: callbacks.Callbacks
    tasks: util.BackgroundTaskManager
    sessions: Sessions


ROUTES: list[Route] = []


@protocol.define(protocol.INFO_V1_ENDPOINT, ROUTES)
async def info_v1(_querry: protocol.Empty, _body: protocol.Empty, state: State, _request: Request):
    return state.info_ctx.to_dto()


@protocol.define(protocol.INFO_V2_ENDPOINT, ROUTES)
async def info_v2(_querry: protocol.Empty, _body: protocol.Empty, state: State, _request: Request):
    return state.info_ctx.to_dto()


@protocol.define(protocol.REGISTER_ENDPOINT, ROUTES)
async def post_register_endpoint(
    _querry: protocol.Empty, body: dto.DeviceInfo, state: State, request: Request
):
    if request.client is None:
        return Response('No client host', status_code=400)

    state.tasks.add(
        state.callbacks.new_device(protocol.Device(host=request.client.host, info=body))
    )
    return state.info_ctx.to_dto()


@protocol.define(protocol.PREPARE_UPLOAD_ENDPOINT, ROUTES)
async def post_prepare_upload_endpoint(
    _querry: protocol.Empty, body: dto.PrepareUploadRequest, state: State, request: Request
):
    if request.client is None:
        return Response('No client host', status_code=400)

    device = protocol.Device(host=request.client.host, info=body.info)
    files = list(body.files.values())
    ouptputs = await asyncio.gather(*[state.callbacks.accept(device, file) for file in files])
    session_id = str(uuid.uuid4())
    uploads = [
        Upload(id=str(uuid.uuid4()), session_id=session_id, file=file, output=ouptput)
        for file, ouptput in zip(files, ouptputs)
        if ouptput is not None
    ]
    if len(uploads) == 0:
        return Response(status_code=403)
    state.sessions[session_id] = {}
    for upload in uploads:
        state.sessions[session_id][upload.id] = upload
    return dto.PrepareUploadResponse(
        sessionId=session_id, files={upload.file.id: upload.id for upload in uploads}
    )


@protocol.define(protocol.UPLOAD_ENDPOINT, ROUTES)
async def post_upload_endpoint(
    querry: dto.UploadParams, _body: protocol.Empty, state: State, request: Request
):
    session = state.sessions.get(querry.sessionId)
    if session is None:
        return Response('Invalid sessionId', status_code=400)
    upload = session.get(querry.token)
    if upload is None:
        return Response('Invalid token', status_code=400)
    if upload.file.id != querry.fileId:
        return Response('Invalid fileId', status_code=400)

    async with upload.output as file:
        async for chunk in request.stream():
            await file.write(chunk)

    return Response()


@protocol.define(protocol.CANCEL_ENDPOINT, ROUTES)
async def post_cancel_endpoint(
    querry: dto.CancelParams, _body: protocol.Empty, state: State, _request: Request
):
    if querry.sessionId is not None:
        with contextlib.suppress(KeyError):
            del state.sessions[querry.sessionId]
    return Response()


def create_app(
    config: Config, info_ctx: info.Context, ready: asyncio.Event, callbacks: callbacks.Callbacks
):
    @contextlib.asynccontextmanager
    async def lifespan(_: Starlette):
        ready.set()
        state = State(config, info_ctx, callbacks, tasks=util.BackgroundTaskManager(), sessions={})
        yield {'state': state}

    return Starlette(debug=config.dev_mode, routes=ROUTES, lifespan=lifespan)


@contextlib.contextmanager
def get_uvicorn_config(config: Config, info_ctx: info.Context, app: Starlette):
    uvicorn_config = uvicorn.Config(
        app=app,
        host=str(config.host),
        port=info_ctx.port,
        lifespan='on',
        ws='none',
        interface='asgi3',
        loop='uvloop' if not config.dev_mode else 'asyncio',
        workers=config.workers or os.cpu_count() or 1 if not config.dev_mode else 1,
    )

    with util.optional_context(
        info_ctx.ssl_ctx.create_files() if info_ctx.ssl_ctx is not None else None
    ) as ssl_files:
        if ssl_files is not None:
            uvicorn_config.ssl_keyfile = ssl_files.key
            uvicorn_config.ssl_keyfile_password = ssl_files.key_password
            uvicorn_config.ssl_certfile = ssl_files.cert
        yield uvicorn_config


async def serve(
    config: Config, info_ctx: info.Context, ready: asyncio.Event, callbacks: callbacks.Callbacks
):
    app = create_app(config, info_ctx, ready, callbacks)
    with get_uvicorn_config(config, info_ctx, app) as uvicorn_config:
        await uvicorn.Server(uvicorn_config).serve()
