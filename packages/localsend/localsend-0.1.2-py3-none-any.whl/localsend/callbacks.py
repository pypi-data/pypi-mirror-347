import dataclasses
import typing

from localsend.lib import dto, protocol


class AsyncWritableIO(typing.Protocol):
    async def write(self, b: bytes, /) -> int: ...


AcceptResult: typing.TypeAlias = typing.AsyncContextManager[AsyncWritableIO]


Accept: typing.TypeAlias = typing.Callable[
    [protocol.Device, dto.File], typing.Awaitable[AcceptResult | None]
]


async def default_accept(_device: protocol.Device, _file: dto.File):
    return None


NewDevice: typing.TypeAlias = typing.Callable[[protocol.Device], typing.Awaitable[None]]


async def default_new_device(_device: protocol.Device):
    return None


@dataclasses.dataclass
class Callbacks:
    accept: Accept = default_accept
    new_device: NewDevice = default_new_device
