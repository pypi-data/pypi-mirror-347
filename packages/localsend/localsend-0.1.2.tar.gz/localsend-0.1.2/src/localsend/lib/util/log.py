import logging
import sys

LOGGER = logging.getLogger("street-service")
FORMATTER = logging.Formatter(
    "[%(levelname)s %(asctime)s.%(msecs)03d] %(message)s", datefmt="%H:%M:%S"
)


def setup_logger():
    LOGGER.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(FORMATTER)
    LOGGER.addHandler(handler)


setup_logger()
