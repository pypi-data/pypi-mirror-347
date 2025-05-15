import dataclasses
import random
import secrets

import pydantic

from localsend.lib import datadir, dto, resources, ssl, util


class Config(pydantic.BaseModel):
    alias: str | None = None
    port: int = 53317
    device_model: str | None = None
    device_type: dto.DeviceType | None = dto.DeviceType.HEADLESS
    protocol_version: dto.StrVersion = dto.Version(2, 1)


def get_alias(config: Config):
    if config.alias is not None:
        return config.alias

    return datadir.cache_text_state(
        'alias',
        lambda: ' '.join(
            random.choice(util.load_word_list(path)).capitalize()
            for path in [resources.get_adjectives_path(), resources.get_object_names_path()]
        ),
    )


def generate_finger_print():
    return secrets.token_hex(32).upper()


def get_fingerprint(ssl_ctx: ssl.Context | None):
    if ssl_ctx is not None:
        return ssl_ctx.certificate_hash

    return datadir.cache_text_state('fingerprint', lambda: secrets.token_hex(16))


@dataclasses.dataclass
class Context:
    ssl_ctx: ssl.Context | None
    alias: str
    fingerprint: str
    port: int
    device_model: str | None
    device_type: dto.DeviceType | None
    protocol_version: dto.StrVersion

    @staticmethod
    def create(config: Config, ssl_ctx: ssl.Context | None):
        return Context(
            ssl_ctx=ssl_ctx,
            alias=get_alias(config),
            fingerprint=get_fingerprint(ssl_ctx),
            port=config.port,
            device_model=config.device_model,
            device_type=config.device_type,
            protocol_version=config.protocol_version,
        )

    def to_dto(self, *, download: bool = False, announce: bool = False):
        return dto.DeviceInfo(
            alias=self.alias,
            version=self.protocol_version,
            fingerprint=self.fingerprint,
            port=self.port,
            protocol=dto.DeviceProtocol.HTTPS
            if self.ssl_ctx is not None
            else dto.DeviceProtocol.HTTP,
            deviceModel=self.device_model,
            deviceType=self.device_type,
            download=download,
            announce=announce,
        )
