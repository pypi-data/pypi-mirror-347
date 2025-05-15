import pathlib
import secrets
import typing

import pydantic
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from localsend.lib import datadir


class Config(pydantic.BaseModel):
    public_exponent: int = 65537
    key_size: int = 2048
    private_key_password: bytes | None = None
    runtime_password_nbytes: int = 64


PrivateKey: typing.TypeAlias = rsa.RSAPrivateKey


def generate(config: Config):
    return rsa.generate_private_key(
        public_exponent=config.public_exponent,
        key_size=config.key_size,
    )


def dump(key: rsa.RSAPrivateKey, config: Config):
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=(
            serialization.NoEncryption()
            if config.private_key_password is None
            else serialization.BestAvailableEncryption(config.private_key_password)
        ),
    )


def load(content: bytes, config: Config):
    private_key = serialization.load_pem_private_key(
        content, password=config.private_key_password
    )
    assert isinstance(private_key, rsa.RSAPrivateKey), type(private_key)
    return private_key


def get_private_key(config: Config) -> PrivateKey:
    return datadir.cache_state(
        name="rsa_private_key.pem",
        create=lambda: generate(config),
        load=lambda content: load(content, config),
        dump=lambda key: dump(key, config),
        max_age=None,
    )


def create_keyfile_password(config: Config):
    return secrets.token_hex(config.runtime_password_nbytes)


def create_key_file(
    private_key: PrivateKey, keyfile_password: str, dir: pathlib.Path, config: Config
):
    dir.mkdir(parents=True, exist_ok=True)
    path = dir / "key.pem"
    path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(
                keyfile_password.encode()
            ),
        )
    )
    return path
