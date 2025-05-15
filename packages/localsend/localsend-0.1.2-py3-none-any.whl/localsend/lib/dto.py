import dataclasses
import datetime
import enum
import typing

import pydantic

from localsend.lib import util


@dataclasses.dataclass
class Version:
    major: int
    minor: int

    @staticmethod
    def load(s: str):
        major, minor = map(int, s.split('.'))
        return Version(major=major, minor=minor)

    def dump(self):
        return '.'.join(map(str, [self.major, self.minor]))


StrVersion: typing.TypeAlias = typing.Annotated[
    Version, *util.annotate_str(Version, Version.dump, Version.load)
]


class DeviceType(enum.Enum):
    MOBILE = 'mobile'
    DESKTOP = 'desktop'
    WEB = 'web'
    HEADLESS = 'headless'
    SERVER = 'server'


class DeviceProtocol(enum.Enum):
    HTTP = 'http'
    HTTPS = 'https'


class PartialDeviceInfo(pydantic.BaseModel):
    alias: str
    version: StrVersion
    fingerprint: str
    deviceModel: str | None
    deviceType: DeviceType | None
    download: bool = False
    announce: bool = False


class DeviceInfo(PartialDeviceInfo):
    port: int
    protocol: DeviceProtocol


class FileMetadata(pydantic.BaseModel):
    modified: datetime.datetime | None = None
    accessed: datetime.datetime | None = None


class File(pydantic.BaseModel):
    id: str
    fileName: str
    size: pydantic.ByteSize
    fileType: str
    sha256: str | None = None
    preview: str | None = None
    metadata: FileMetadata = pydantic.Field(default_factory=FileMetadata)


class PrepareUploadRequest(pydantic.BaseModel):
    info: DeviceInfo
    files: dict[str, File]


class PrepareUploadResponse(pydantic.BaseModel):
    sessionId: str
    files: dict[str, str]


class UploadParams(pydantic.BaseModel):
    sessionId: str
    fileId: str
    token: str


class CancelParams(pydantic.BaseModel):
    sessionId: str | None = None
