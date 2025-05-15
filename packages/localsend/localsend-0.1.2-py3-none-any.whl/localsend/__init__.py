import importlib.metadata
import pathlib

from .app import App, create_app
from .callbacks import Callbacks
from .config import Config
from .lib.dto import File as FileDto
from .lib.protocol import Device
from .upload import File

__module_dir__ = pathlib.Path(__file__).absolute().parent
__package_name__ = __module_dir__.name
__version__ = importlib.metadata.version(__package_name__)
__all__ = ['App', 'create_app', 'Callbacks', 'Config', 'Device', 'File', 'FileDto']
