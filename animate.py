import os
import re
from pathlib import Path
from datetime import datetime
import pandas as pd

def create_gif(image_folder='images',
               output_file='timelapse.mp4',
               framerate=None,
               **kwargs):
    if not isinstance(image_folder, Path):
        image_folder = Path(image_folder)
    if not image_folder.is_absolute():
        image_folder = image_folder.resolve()

    setup_images(image_folder, **kwargs)
    cmd = 'ffmpeg -y'
    cmd += ' -f concat -safe 0 -i {}'.format('gif_files.txt')
    if framerate is not None:
        cmd += ' -framerate {}'.format(framerate)
    cmd += ' {}'.format(output_file)
    os.system(cmd)


def setup_images(path,
                 start=None,
                 end=None,
                 size=10**6,
                 shorten_dark=None,
                 downsample=None):
    if not isinstance(path, Path):
        path = Path(path)
    assert  isinstance(path, Path)

    images = [f for f in path.glob('*.jpg')]

    df = pd.DataFrame({
        'Time': [timestamp(f) for f in images],
        'Path': images,
        'Size': [f.stat().st_size for f in images]
    }).set_index('Time')

    if start is not None:
        df = df[start:]
    if end is not None:
        df = df[:end]
    if size is not None:
        size_mask = df['Size'] > size
        if shorten_dark is not None:
            df = pd.concat([df[size_mask], df[~size_mask].iloc[::shorten_dark]]).sort_index()
        else:
            df = df[size_mask]
    if downsample is not None:
        assert isinstance(downsample, int)
        df = df[::downsample]

    FILE = Path.cwd() / 'gif_files.txt'
    with open(FILE, 'w') as file:
        for i, row in df.iterrows():
            file.write('file \'{}\'\n'.format(row['Path'].relative_to(Path.cwd())))

    print('{} files set up in {}'.format(len(df), FILE.name))
    return FILE

def timestamp(file):
    time_string = re.match('([\d\-\_]+)_.*', file.stem).group(1)
    return datetime.strptime(time_string, '%Y-%m-%d_%H%M%S')

if __name__ == '__main__':
    create_gif(framerate=60,
               downsample=30,
               size=3*(10**5),
               shorten_dark=15)
