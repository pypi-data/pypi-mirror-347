import logging
from collections import namedtuple

from .exception_util import exception_as_string,exceptions_as_string
from .conditional_sleep import sleep_with_condition
from .value_to_bool import value_to_bool

__all__ = (
    "exception_as_string","exceptions_as_string",
    "async_util",
    "caching",
    "sleep_with_condition",
    "hibp",
    "value_to_bool",
    "timing",
)
__version__ = "1.6.1"
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=1, minor=6, micro=1, releaselevel="final", serial=0)
logging.getLogger(__name__).addHandler(logging.NullHandler())
