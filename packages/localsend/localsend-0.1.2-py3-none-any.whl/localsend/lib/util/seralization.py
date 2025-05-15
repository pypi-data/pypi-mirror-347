import pathlib
import typing

import pydantic


def annotate_str[T](
    type: type[T],
    serializer: typing.Callable[[T], str],
    deserializer: typing.Callable[[str], T | None],
):
    def validator(v: object):
        if isinstance(v, str):
            deser_v = deserializer(v)
            if deser_v is not None:
                return deser_v
            raise ValueError(f"Value is not a valid {type.__name__}")
        return v

    return (
        pydantic.BeforeValidator(validator),
        pydantic.PlainSerializer(serializer),
        pydantic.WithJsonSchema({"type": "string", "format": type.__name__}),
    )


def load_word_list(path: pathlib.Path):
    return [
        word.lower()
        for line in path.read_text().splitlines()
        if len(word := line.strip()) > 0
    ]


IP_TYPE_ADAPTER = pydantic.TypeAdapter[pydantic.IPvAnyAddress](pydantic.IPvAnyAddress)
