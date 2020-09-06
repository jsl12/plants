import ftplib
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from pvlib import solarposition

from .devices import RPI_3

LOGGER = logging.getLogger(__name__)

FILE_REGEX = re.compile('image_(\d+)\.jpg$')

DATE_REGEX = re.compile('\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')


def dated_files(base: Path, glob: str = '*.*', time_zone: str = 'US/Central') -> pd.Series:
    s = pd.Series([f for f in base.glob(glob) if DATE_REGEX.match(f.name)])
    s.index = pd.DatetimeIndex(s.apply(lambda s:datetime.strptime(s.name[:19], '%Y-%m-%d_%H-%M-%S'))).tz_localize(time_zone)
    s = s.sort_index()
    return s


def positioned_files(base: Path, glob: str = '*.*') -> pd.Series:
    files = dated_files(base, glob)
    pos = solarposition.get_solarposition(files.index, 30.250657, -97.748108)
    pos['path'] = files
    return pos


def filter_time(base: Path, glob: str = '*.*',  start = None, end = None) -> pd.Series:
    """
    Returns a Series of paths filtered by start/stop times enocded with the pattern

    :param base:
    :param start:
    :param end:
    :return:
    """

    s = dated_files(base, glob)

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


def convert_files(source: Path, name: str, glob: str = '*.jpg'):
    files = sorted([f for f in source.glob(glob)], key=lambda f: f.name)
    for f in files:
        convert_filename(f, name=name)


def send_file(file: Path, dest_folder: Path = None):
    dest = (dest_folder / file.name) if dest_folder is not None else Path(file.name)
    with ftplib.FTP(*RPI_3) as conn:
        LOGGER.info(f'Opened connection to {RPI_3[1]}:{RPI_3[2]}@{RPI_3[0]}')
        try:
            LOGGER.info(f'Sending file to {dest.as_posix()}')
            conn.storbinary(f'STOR {dest.as_posix()}', file.open('rb'))
        except ftplib.error_perm as e:
            print(e)
            print(dest.as_posix())
        else:
            LOGGER.info(f'Success')
