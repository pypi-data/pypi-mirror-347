"""Theia dumper package."""

from importlib.metadata import version, PackageNotFoundError
from .logger import logger

try:
    __version__ = version("theia_dumper")
except PackageNotFoundError:
    pass

logger.warning(
    "The 'theia-dumper' package is now deprecated. "
    "Please use the 'teledetection' package instead. "
    "See https://github.com/teledec/teledetection."
)
