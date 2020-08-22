import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

FILE_REGEX = re.compile('image_(\d+)\.jpg$')

LOGGER = logging.getLogger(__name__)


def filter_time(base: Path, start = None, end = None):
    rgx = re.compile('\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')
    s = pd.Series([f for f in base.glob('*.*') if rgx.match(f.name)])
    s.index = s.apply(lambda s:datetime.strptime(s.name[:19], '%Y-%m-%d_%H-%M-%S'))
    s = s.sort_index()

    if start is not None:
        s = s[start:]

    if end is not None:
        s = s[:end]

    return s


def convert_filename(path: Path, name:str):
    """
    Converts the files with timestamps created by raspistill into formatted date strings with 'name' as a suffix

    :param path:
    :param name:
    :return:
    """
    if match := FILE_REGEX.match(path.name):
        pic_date = datetime.fromtimestamp(int(match.group(1)))
        if (datetime.now() - pic_date) >= timedelta(minutes=2):
            new_filename = path.with_name(f'{pic_date.strftime("%Y-%m-%d_%H-%M-%S")}_{name}').with_suffix(path.suffix)
            try:
                path.rename(new_filename)
            except FileExistsError:
                LOGGER.info(f'File already exists: {new_filename}')
                return
            else:
                LOGGER.info(f'Renamed {path.name} to {new_filename.name}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    for f in Path(r'H:\temp\plants').glob('*.jpg'):
        convert_filename(f, 'patio')
