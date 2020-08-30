from datetime import datetime
from pathlib import Path

from .animate import timelapse
from .file import convert_filename
from .file import positioned_files
from .temp import read_temp


def day(
        base: Path,
        output_folder: Path,
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
        output=output_folder / f'{datetime.now().strftime("%Y-%m-%d")}_{suffix or "daybreak"}.mp4',
        **kwargs
    )

def convert_files(source: Path, name: str, glob: str = '*.jpg'):
    files = sorted([f for f in source.glob(glob)], key=lambda f: f.name)
    for f in files:
        convert_filename(f, name=name)
