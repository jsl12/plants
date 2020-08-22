import logging
from pathlib import Path

import ffmpeg

LOGGER = logging.getLogger(__name__)

def write_filelist(path: Path, filepaths):
    with path.open('w') as file:
        file.writelines([f'file {f.as_posix()}\n' for f in filepaths])


def make_gif(files, output, framerate = None, overwrite: bool = True):
    # http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
    # https://engineering.giphy.com/how-to-make-gifs-with-ffmpeg/
    LOGGER.info(f'Concatenating {len(files)} files into {output}')
    output_kwargs = {}
    if framerate is not None:
        output_kwargs['framerate'] = framerate

    temp_filelist = files[0].with_name('filelist.txt')
    write_filelist(temp_filelist, sorted(files, key=lambda f:f.name))

    input = ffmpeg.input(temp_filelist, format='concat', safe=0)
    split = input.filter_multi_output('split')
    (
        ffmpeg.filter(
            [split[0], split[1].filter('palettegen', stats_mode='diff')],
            filter_name='paletteuse',
            dither='bayer'
        )
        .output(output.as_posix(), **output_kwargs)
        .run(overwrite_output=overwrite)
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    p = Path(r'H:\temp\plants')
    files = [f for f in p.glob('*_patio.jpg')]
    make_gif(files, Path(r'C:\Users\lanca\OneDrive\Documents\Software\Plants\temp\test.gif'), framerate=30)
