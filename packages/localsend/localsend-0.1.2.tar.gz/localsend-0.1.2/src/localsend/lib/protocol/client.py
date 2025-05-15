import dataclasses
import typing
import urllib.parse

import httpx
import pydantic

from localsend.lib import dto, util

from . import device, endpoints

RawBody: typing.TypeAlias = str | bytes | typing.Iterable[bytes] | typing.AsyncIterable[bytes]


def get_device_url(host: str, info: dto.DeviceInfo):
    return f'{info.protocol.value}://{host}:{info.port}'


@dataclasses.dataclass
class InvalidCall(Exception):
    url: httpx.URL
    status_code: int
    text: str
    headers: httpx.Headers


async def _call[Q: pydantic.BaseModel, ReqB: pydantic.BaseModel, ResB: pydantic.BaseModel](
    spec: endpoints.Endpoint[Q, ReqB, ResB],
    device: device.Device,
    querry: Q,
    body: ReqB | RawBody,
    http_client: httpx.AsyncClient,
    headers: dict[str, str] | None = None,
) -> tuple[ResB, httpx.Response]:
    if headers is None:
        headers = {}

    url = urllib.parse.urlunparse(
        urllib.parse.ParseResult(
            scheme=device.info.protocol.value,
            netloc=f'{device.host}:{device.info.port}',
            path=spec.path,
            params='',
            query=urllib.parse.urlencode(
                [(k, str(v)) for k, v in querry.model_dump(mode='json').items()]
            ),
            fragment='',
        )
    )

    if isinstance(body, pydantic.BaseModel):
        content = body.model_dump_json(by_alias=True).encode()
        headers['Content-Type'] = 'application/json'
    else:
        content = body

    response = await http_client.request(
        method=spec.method, url=url, content=content, headers=headers
    )

    if response.status_code != 200:
        raise InvalidCall(
            url=response.url,
            status_code=response.status_code,
            text=response.text,
            headers=response.headers,
        )

    if issubclass(spec.response_body, endpoints.Empty):
        return (spec.response_body.model_validate({}), response)

    try:
        return (spec.response_body.model_validate_json(response.content), response)
    except pydantic.ValidationError as exc:
        util.LOGGER.info(f'Error while validating response {exc}, {response.content}')
        raise


_EMPTY = endpoints.Empty()


@dataclasses.dataclass
class Client:
    http_client: httpx.AsyncClient

    async def call_info_v1(self, device: device.Device):
        return (await _call(endpoints.INFO_V1_ENDPOINT, device, _EMPTY, _EMPTY, self.http_client))[
            0
        ]

    async def call_info_v2(self, device: device.Device):
        return (await _call(endpoints.INFO_V2_ENDPOINT, device, _EMPTY, _EMPTY, self.http_client))[
            0
        ]

    async def call_register(self, device: device.Device, body: dto.DeviceInfo):
        return (
            await _call(
                endpoints.REGISTER_ENDPOINT, device, endpoints.Empty(), body, self.http_client
            )
        )[0]

    async def call_prepare_upload(self, device: device.Device, body: dto.PrepareUploadRequest):
        return (
            await _call(
                endpoints.PREPARE_UPLOAD_ENDPOINT, device, endpoints.Empty(), body, self.http_client
            )
        )[0]

    async def call_upload(self, device: device.Device, params: dto.UploadParams, body: RawBody):
        return (await _call(endpoints.UPLOAD_ENDPOINT, device, params, body, self.http_client))[0]

    async def call_cancel(self, device: device.Device, params: dto.CancelParams):
        return (await _call(endpoints.CANCEL_ENDPOINT, device, params, _EMPTY, self.http_client))[0]
