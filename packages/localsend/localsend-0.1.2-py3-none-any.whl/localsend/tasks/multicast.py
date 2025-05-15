import contextlib
import dataclasses
import ipaddress
import socket
import threading

import httpx
import multicast_expert
import pydantic

from localsend import callbacks, info
from localsend.lib import dto, protocol, util


class Config(pydantic.BaseModel):
    interface: str | None = None
    group: pydantic.IPvAnyAddress = ipaddress.IPv4Address('224.0.0.167')
    http_client_connections: int = 2


@dataclasses.dataclass
class SocketInfo:
    group_addr: pydantic.IPvAnyAddress
    addr_family: int
    iface: str


@staticmethod
def get_socket_info(config: Config):
    match config.group:
        case ipaddress.IPv4Address():
            addr_family = socket.AF_INET
        case ipaddress.IPv6Address():
            addr_family = socket.AF_INET6
    default_iface = multicast_expert.get_default_gateway_iface_ip(addr_family)
    assert default_iface is not None, addr_family
    return SocketInfo(
        group_addr=config.group, addr_family=addr_family, iface=config.interface or default_iface
    )


def create_receive_socket(config: Config, port: int) -> multicast_expert.AsyncMcastRxSocket:
    socket_info = get_socket_info(config)
    return multicast_expert.AsyncMcastRxSocket(
        addr_family=socket_info.addr_family,
        mcast_ips=[socket_info.group_addr],
        port=port,
        iface=socket_info.iface,
    )


def create_send_socket(config: Config) -> multicast_expert.McastTxSocket:
    socket_info = get_socket_info(config)
    return multicast_expert.McastTxSocket(
        addr_family=socket_info.addr_family,
        mcast_ips=[socket_info.group_addr],
        iface=socket_info.iface,
    )


@contextlib.asynccontextmanager
async def create_client(config: Config):
    async with httpx.AsyncClient(
        verify=False, limits=httpx.Limits(max_connections=config.http_client_connections)
    ) as http_client:
        yield protocol.Client(http_client)


async def receive(callbacks: callbacks.Callbacks, config: Config, info_ctx: info.Context):
    tasks = util.BackgroundTaskManager()
    try:
        async with create_client(config) as client:
            with create_receive_socket(config, info_ctx.port) as sock:
                util.LOGGER.info('Waiting for multicast messages')
                while True:
                    content, (host, *_) = await sock.recvfrom()
                    util.LOGGER.info(f'Received message from {host}')
                    device_info = dto.DeviceInfo.model_validate_json(content)
                    device = protocol.Device(host, device_info)
                    tasks.add(callbacks.new_device(device))
                    await client.call_register(device, info_ctx.to_dto())
    finally:
        util.LOGGER.info('Stopped receiving multicast messages')


def send_sync(config: Config, info: info.Context, _cancel: threading.Event):
    message = info.to_dto(announce=True).model_dump_json(by_alias=True).encode()
    with create_send_socket(config) as sock:
        util.LOGGER.info('Sending multicast message')
        sock.sendto(message, (str(config.group), info.port))


async def send(config: Config, info: info.Context):
    await util.wait_sync(lambda cancel: send_sync(config, info, cancel))
