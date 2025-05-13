import openvino  # noqa
from ._core import load_and_compile_model
from ._version import __version__

__all__ = ["get_available_devices", "load_and_compile_model", "__version__"]
