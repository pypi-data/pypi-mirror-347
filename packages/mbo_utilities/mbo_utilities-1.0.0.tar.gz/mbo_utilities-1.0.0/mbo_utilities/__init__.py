from pathlib import Path

from .file_io import (
    get_files,
    zstack_from_files,
    npy_to_dask,
    read_scan,
    save_png,
    save_mp4,
    zarr_to_dask,
    expand_paths,
)
from .assembly import save_as
from .metadata import is_raw_scanimage, get_metadata, params_from_metadata
from .image import fix_scan_phase, return_scan_offset
from .util import (
    norm_minmax,
    smooth_data,
    is_running_jupyter,
    is_imgui_installed,
    is_qt_installed,
    subsample_array,
)

from .graphics import run_gui

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()

__all__ = [
    "run_gui",
    # image processing
    "fix_scan_phase",
    "return_scan_offset",
    # file_io
    "scanreader",
    "npy_to_dask",
    "zarr_to_dask",
    "get_files",
    "zstack_from_files",
    "read_scan",
    "save_png",
    "save_mp4",
    "expand_paths",
    "subsample_array",
    # metadata
    "is_raw_scanimage",
    "get_metadata",
    "params_from_metadata",
    # util
    "norm_minmax",
    "smooth_data",
    "is_running_jupyter",
    "is_qt_installed",
    "is_imgui_installed",
    # assembly
    "save_as",
]
