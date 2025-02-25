import logging
from pathlib import Path

import ffmpeg

LOGGER = logging.getLogger(__name__)


def write_filelist(path: Path, filepaths):
    with path.open('w') as file:
        file.writelines([f'file {f.as_posix()}\n' for f in filepaths])


def timelapse(files, output, framerate = None, overwrite: bool = True, colors=False, scale: str = None):
    # http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
    # https://engineering.giphy.com/how-to-make-gifs-with-ffmpeg/
    LOGGER.info(f'Concatenating {len(files)} files into {output}')
    output_kwargs = {}
    if framerate is not None:
        output_kwargs['framerate'] = framerate

    if files:
        temp_filelist = files[0].with_name('filelist.txt')
        write_filelist(temp_filelist, sorted(files, key=lambda f:f.name))
    else:
        raise ValueError(f'No files')

    input = ffmpeg.input(temp_filelist, format='concat', safe=0)
    if scale is not None:
        input = input.filter('scale', scale, force_original_aspect_ratio='decrease')
    (
        input
        .output(output.with_suffix('.mp4').as_posix(), **output_kwargs)
        .run(overwrite_output=overwrite)
    )

    if colors:
        improve_colors(input=output, output=output.with_name(f'{output.stem}_colors{output.suffix}'))


def improve_colors(input: Path, output: Path, overwrite:bool = True):
    LOGGER.info(f'Starting color improvement')
    input = ffmpeg.input(input).filter_multi_output('split')
    (
        ffmpeg.filter(
            [input[0], input[1].filter('palettegen', stats_mode='diff')],
            filter_name='paletteuse',
            dither='bayer'
        )
        .output(output.with_suffix('.gif').as_posix())
        .run(overwrite_output=overwrite)
    )
