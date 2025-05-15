import contextlib
import datetime
import pathlib
import shutil
import tempfile
import tomllib
import typing

import platformdirs

import localsend
from localsend.lib import util


def get_local_project_dir():
    local_project_dir = localsend.__module_dir__.parent.parent
    pyproject_path = local_project_dir / "pyproject.toml"
    with contextlib.suppress(FileNotFoundError):
        pyproject = tomllib.loads(pyproject_path.read_text())
        if pyproject.get("project", {}).get("name") == localsend.__package_name__:
            return local_project_dir
    return None


def _get_dir(
    realease_factory: typing.Callable[[platformdirs.PlatformDirs], str], local_name: str
):
    match get_local_project_dir():
        case pathlib.Path() as local_project_dir:
            return local_project_dir / local_name
        case None:
            return pathlib.Path(
                realease_factory(
                    platformdirs.PlatformDirs(appname="com.floriand.LocalSend")
                )
            ).absolute()


def get_state_dir():
    return _get_dir(realease_factory=lambda p: p.user_state_dir, local_name=".state")


def get_runtime_dir():
    return _get_dir(
        realease_factory=lambda p: p.user_runtime_dir, local_name=".runtime"
    )


def get_cache_dir():
    return _get_dir(realease_factory=lambda p: p.user_cache_dir, local_name=".cache")


def get_config_dir():
    return _get_dir(realease_factory=lambda p: p.user_config_dir, local_name=".config")


def get_downloads_dir():
    return _get_dir(
        realease_factory=lambda p: p.user_downloads_dir, local_name=".downloads"
    )


@contextlib.contextmanager
def create_tmp_dir():
    base_dir = get_runtime_dir() / "tmp"
    base_dir.mkdir(parents=True, exist_ok=True)
    dir_path = pathlib.Path(tempfile.mkdtemp(dir=base_dir, prefix=""))
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path, ignore_errors=True)


def _cache[T](
    path: pathlib.Path,
    *,
    create: typing.Callable[[], T],
    load: typing.Callable[[bytes], T],
    dump: typing.Callable[[T], bytes],
    max_age: datetime.timedelta | None,
) -> T:
    if (max_age is None) or (age := util.get_file_age(path)) is None or (age < max_age):
        content = None
        with contextlib.suppress(FileNotFoundError):
            content = path.read_bytes()

        if content is not None:
            return load(content)

    t = create()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(dump(t))
    return t


def cache_state[T](
    name: str | pathlib.Path,
    *,
    create: typing.Callable[[], T],
    load: typing.Callable[[bytes], T],
    dump: typing.Callable[[T], bytes],
    max_age: datetime.timedelta | None,
) -> T:
    return _cache(
        get_state_dir() / name, create=create, load=load, dump=dump, max_age=max_age
    )


def cache_text_state(name: str, create: typing.Callable[[], str]):
    return cache_state(
        f"{name}.txt",
        create=create,
        load=bytes.decode,
        dump=str.encode,
        max_age=None,
    )
