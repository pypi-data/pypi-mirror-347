"""Root package info."""

import os

from litmodels.__about__ import *  # noqa: F401, F403

_PACKAGE_ROOT = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.dirname(_PACKAGE_ROOT)

from litmodels.io import download_model, load_model, save_model, upload_model, upload_model_files  # noqa: F401

__all__ = ["download_model", "upload_model", "load_model", "save_model"]
