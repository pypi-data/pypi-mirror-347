"""Dinamis SDK module."""

# flake8: noqa

from importlib.metadata import version, PackageNotFoundError
from dinamis_sdk.signing import (
    sign,
    sign_inplace,
    sign_urls,
    sign_item,
    sign_asset,
    sign_item_collection,
    sign_url_put,
)  # noqa
from .oauth2 import OAuth2Session  # noqa
from .upload import push
from .http import get_headers, get_userinfo, get_username
from .utils import get_logger_for

try:
    __version__ = version("dinamis_sdk")
except PackageNotFoundError:
    pass

get_logger_for(__name__).warning(
    "The 'dinamis-sdk' package is now deprecated. "
    "Please use the 'teledetection' package instead. "
    "See https://github.com/teledec/teledetection."
)
