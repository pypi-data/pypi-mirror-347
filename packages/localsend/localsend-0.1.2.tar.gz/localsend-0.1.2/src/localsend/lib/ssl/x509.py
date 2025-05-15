import datetime
import hashlib
import pathlib
import typing

import pydantic
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from localsend.lib import datadir, util


class Config(pydantic.BaseModel):
    validity: datetime.timedelta = datetime.timedelta(days=365)
    common_name: str = "LocalSend Python"


Certificate: typing.TypeAlias = x509.Certificate


def generate(config: Config, private_key: rsa.RSAPrivateKey):
    now = util.now()
    name = x509.Name([x509.NameAttribute(x509.NameOID.COMMON_NAME, config.common_name)])
    return (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + config.validity)
        .sign(private_key, hashes.SHA256())
    )


def dump(certificate: x509.Certificate):
    return certificate.public_bytes(serialization.Encoding.PEM)


def load(content: bytes):
    return x509.load_pem_x509_certificate(content)


def get_certificate(config: Config, private_key: rsa.RSAPrivateKey) -> Certificate:
    return datadir.cache_state(
        name="x509_certificate.pem",
        create=lambda: generate(config, private_key),
        load=load,
        dump=dump,
        max_age=config.validity,
    )


def create_cert_file(certificate: Certificate, dir: pathlib.Path):
    dir.mkdir(parents=True, exist_ok=True)
    path = dir / "cert.pem"
    path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    return path


def compute_certificate_hash(certificate: Certificate):
    return (
        hashlib.sha256(certificate.public_bytes(serialization.Encoding.DER))
        .hexdigest()
        .upper()
    )
