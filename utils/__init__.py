from datetime import datetime
from pathlib import Path

from utils.animate import timelapse
from utils.file import filter_time
from utils.sun import get_twilights


def daybreak(source: Path, output_folder: Path, **kwargs):
    df = get_twilights()
    files = filter_time(
        source,
        start=df.loc['Civil Twilight', 'Begin'].iloc[0],
        end=df.loc['Civil Twilight', 'End'].iloc[1]
    )
    timelapse(
        files=files.to_list(),
        output=output_folder / f'{datetime.now().strftime("%Y-%m-%d")}_daybreak.mp4',
        **kwargs
    )
