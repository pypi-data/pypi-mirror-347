import contextlib


@contextlib.contextmanager
def add_exception_note(note: str):
    try:
        yield
    except BaseException as exc:
        exc.add_note(note)
        raise
