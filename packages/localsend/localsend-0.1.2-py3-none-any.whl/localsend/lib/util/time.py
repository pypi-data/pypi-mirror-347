import dataclasses
import datetime


def now():
    return datetime.datetime.now(tz=datetime.UTC)


@dataclasses.dataclass
class Dated[T]:
    value: T
    at: datetime.datetime
