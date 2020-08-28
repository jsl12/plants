from datetime import datetime
from pathlib import Path

from .animate import timelapse
from .file import convert_filename
from .file import filter_time
from .sun import get_twilights


def day(source: Path, output_folder: Path, suffix: str = None, downsample: int = None, **kwargs):
    df = get_twilights()
    files = filter_time(
        source,
        start=df.loc['Civil Twilight', 'Begin'].iloc[0],
        end=df.loc['Civil Twilight', 'End'].iloc[1]
    )
    files = files.iloc[::downsample]
    timelapse(
        files=files.to_list(),
        output=output_folder / f'{datetime.now().strftime("%Y-%m-%d")}_{suffix or "daybreak"}.mp4',
        **kwargs
    )

def convert_files(source: Path, name: str, glob: str = '*.jpg'):
    files = sorted([f for f in source.glob(glob)], key=lambda f: f.name)
    for f in files:
        convert_filename(f, name=name)
