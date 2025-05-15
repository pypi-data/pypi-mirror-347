import dataclasses
import typing

import pydantic

from localsend.lib import dto


class Empty(pydantic.BaseModel):
    pass


@dataclasses.dataclass
class Endpoint[Q: pydantic.BaseModel, ReqB: pydantic.BaseModel, ResB: pydantic.BaseModel]:
    method: typing.Literal['GET', 'POST']
    path: str
    querry: type[Q]
    request_body: type[ReqB]
    response_body: type[ResB]


INFO_V1_ENDPOINT = Endpoint(
    method='GET',
    path='/api/localsend/v1/info',
    querry=Empty,
    request_body=Empty,
    response_body=dto.PartialDeviceInfo,
)

INFO_V2_ENDPOINT = Endpoint(
    method='GET',
    path='/api/localsend/v2/info',
    querry=Empty,
    request_body=Empty,
    response_body=dto.PartialDeviceInfo,
)

REGISTER_ENDPOINT = Endpoint(
    method='POST',
    path='/api/localsend/v2/register',
    querry=Empty,
    request_body=dto.DeviceInfo,
    response_body=dto.PartialDeviceInfo,
)


PREPARE_UPLOAD_ENDPOINT = Endpoint(
    method='POST',
    path='/api/localsend/v2/prepare-upload',
    querry=Empty,
    request_body=dto.PrepareUploadRequest,
    response_body=dto.PrepareUploadResponse,
)


UPLOAD_ENDPOINT = Endpoint(
    method='POST',
    path='/api/localsend/v2/upload',
    querry=dto.UploadParams,
    request_body=Empty,
    response_body=Empty,
)

CANCEL_ENDPOINT = Endpoint(
    method='POST',
    path='/api/localsend/v2/cancel',
    querry=dto.CancelParams,
    request_body=Empty,
    response_body=Empty,
)
