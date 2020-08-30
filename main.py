import logging
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Tuple

import click
import pandas as pd
from picamera import PiCamera
from pvlib import solarposition

from utils.temp import read_temp

LOGGER = logging.getLogger(__name__)

@click.command()
@click.option('--sensor_mode', '-m', type=int, default=0)
@click.option('--resolution', '-res', type=(int, int), default=(None, None))
@click.option('--res_folder', '-rf', type=click.Path(exists=True), default='/mnt/nas/')
@click.option('--name', '-n', type=str)
@click.option('--text_size', '-ts', type=int, default=None)
@click.option('--min_elevation', '-e', type=int, default=-18)
def take_picture(
        sensor_mode: int,
        resolution: Tuple[int],
        res_folder: str,
        name: str,
        text_size: int,
        min_elevation:int
):
    pos = solarposition.get_solarposition(
        pd.DatetimeIndex([datetime.now()], tz='US/Central'),
        30.250657,
        -97.748108
    ).iloc[0]

    try:
        cam = PiCamera(sensor_mode=sensor_mode, resolution=None if resolution[0] is None else resolution)
    except Exception as e:
        LOGGER.exception(e)
        return
    else:
        LOGGER.info(f'Sleeping for initialization...')
        sleep(2)
        LOGGER.info(f'PiCamera initialized: Mode {cam.sensor_mode} - {cam.resolution[0]}x{cam.resolution[1]}')

    pic_date = datetime.now()

    if text_size is not None:
        cam.annotate_text = f'{pic_date.strftime("%Y-%m-%d %H:%M:%S")}, Elevation: {pos.apparent_elevation:.1f}, Azimuth: {pos.azimuth:.1f}, Temp: {read_temp():.1f} C'
        cam.annotate_text_size = text_size

    res_file = Path(res_folder) / f'{pic_date.strftime("%Y-%m-%d_%H-%M-%S")}_{name}.jpg'

    if pos.apparent_elevation >= min_elevation:
        try:
            cam.capture(res_file.as_posix())
        except Exception as e:
            LOGGER.exception(e)
            return
        else:
            LOGGER.info(f'Captured to {res_file.name}')
        finally:
            cam.close()
    else:
        LOGGER.info(pic_date)
        LOGGER.info(f'Apparent elevation too low: {pos.apparent_elevation:.2f}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    take_picture()
