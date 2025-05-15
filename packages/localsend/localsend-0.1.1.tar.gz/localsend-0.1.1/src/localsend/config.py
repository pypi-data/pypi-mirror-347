import typing

import pydantic

from localsend import info, upload
from localsend.lib import ssl
from localsend.tasks import http_server, multicast

SslConfig = ssl.Config
HttpServerConfig = http_server.Config
MulticaseConfig = multicast.Config
InfoConfig = info.Config
UploadConfig = upload.Config


class Config(pydantic.BaseModel):
    ssl: SslConfig | typing.Literal["disabled"] = pydantic.Field(
        default_factory=SslConfig
    )
    http_server: HttpServerConfig = pydantic.Field(default_factory=HttpServerConfig)
    multicast: MulticaseConfig = pydantic.Field(default_factory=MulticaseConfig)
    info: InfoConfig = pydantic.Field(default_factory=InfoConfig)
    upload: UploadConfig = pydantic.Field(default_factory=UploadConfig)
