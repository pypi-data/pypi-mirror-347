import dataclasses

from localsend.lib import dto


@dataclasses.dataclass(frozen=True)
class Device:
    host: str
    info: dto.DeviceInfo
