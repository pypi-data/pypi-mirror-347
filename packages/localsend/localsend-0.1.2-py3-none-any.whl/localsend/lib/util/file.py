import contextlib
import datetime
import pathlib

from . import time


def get_file_last_update_datetime(path: pathlib.Path):
    with contextlib.suppress(OSError):
        return datetime.datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    return None


def get_file_age(path: pathlib.Path):
    update_datetime = get_file_last_update_datetime(path)
    if update_datetime is not None:
        return time.now() - update_datetime
    return None
