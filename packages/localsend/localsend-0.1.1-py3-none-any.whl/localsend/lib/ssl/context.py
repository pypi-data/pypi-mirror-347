import contextlib
import dataclasses
import functools
import pathlib

import pydantic

from localsend.lib import datadir

from . import rsa, x509

X509Config = x509.Config
RsaConfig = rsa.Config


class Config(pydantic.BaseModel):
    x509: X509Config = pydantic.Field(default_factory=X509Config)
    rsa: RsaConfig = pydantic.Field(default_factory=RsaConfig)


@dataclasses.dataclass(frozen=True)
class Files:
    key: pathlib.Path
    cert: pathlib.Path
    key_password: str


@dataclasses.dataclass(frozen=True)
class Context:
    config: Config
    certificate: x509.Certificate
    private_key: rsa.PrivateKey

    @staticmethod
    def create(config: Config):
        private_key = rsa.get_private_key(config.rsa)
        certificate = x509.get_certificate(config.x509, private_key)
        return Context(config, certificate, private_key)

    @contextlib.contextmanager
    def create_files(self):
        with datadir.create_tmp_dir() as tmp_dir:
            keyfile_password = rsa.create_keyfile_password(self.config.rsa)
            yield Files(
                key=rsa.create_key_file(
                    self.private_key, keyfile_password, tmp_dir, self.config.rsa
                ),
                cert=x509.create_cert_file(self.certificate, tmp_dir),
                key_password=keyfile_password,
            )

    @functools.cached_property
    def certificate_hash(self):
        return x509.compute_certificate_hash(self.certificate)
