import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

FILE_REGEX = re.compile('image_(\d+)\.jpg$')

LOGGER = logging.getLogger(__name__)

def convert_filename(path: Path, name:str):
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
    for f in Path(r'H:\temp\plants').glob('*.jpg'):
        convert_filename(f, 'patio')
