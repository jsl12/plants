import logging
from datetime import datetime
from pathlib import Path

from .animate import timelapse
from .devices import RPI_3, PI_0W
from .file import convert_filename
from .file import positioned_files

LOGGER = logging.getLogger(__name__)


def make_both(**kwargs):
    assert 'suffix' in kwargs
    orig_suffix = kwargs.pop('suffix')
    day(suffix=f'{orig_suffix}_720p', scale='hd720', **kwargs)
    day(suffix=orig_suffix, **kwargs)


def day(
        base: Path,
        output_dir: Path,
        suffix: str = None,
        downsample: int = None,
        min_elevation: int = None,
        max_elevation: int = None,
        increasing: bool = True,
        **kwargs
):
    files = positioned_files(base, '*.jpg')

    if min_elevation is not None:
        files = files[files.apparent_elevation >= min_elevation]

    if max_elevation is not None:
        files = files[files.apparent_elevation <= max_elevation]

    if increasing:
        files = files[files.apparent_elevation.diff() > 0]

    files = files.iloc[::downsample]

    timelapse(
        files=files.path.to_list(),
        output=output_dir / f'{datetime.now().strftime("%Y-%m-%d")}_{suffix or "daybreak"}.mp4',
        **kwargs
    )
