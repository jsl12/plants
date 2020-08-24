from datetime import datetime
from pathlib import Path

from utils.animate import timelapse
from utils.file import filter_time
from utils.sun import get_twilights


def day(source: Path, output_folder: Path, suffix: str = None, **kwargs):
    df = get_twilights()
    files = filter_time(
        source,
        start=df.loc['Civil Twilight', 'Begin'].iloc[0],
        end=df.loc['Civil Twilight', 'End'].iloc[1]
    )
    timelapse(
        files=files.to_list(),
        output=output_folder / f'{datetime.now().strftime("%Y-%m-%d")}_{suffix or "daybreak"}.mp4',
        **kwargs
    )
