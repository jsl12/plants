from datetime import datetime
from pathlib import Path
from time import sleep

import pandas as pd
from picamera import PiCamera
from pvlib import solarposition

if __name__ == '__main__':
    pos = solarposition.get_solarposition(
        pd.DatetimeIndex([datetime.now()], tz='US/Central'),
        30.250657,
        -97.748108
    ).iloc[0]
    pos_str = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nElevation: {pos.elevation:.2f}, Azimuth: {pos.azimuth:.2f}'

    if pos['elevation'] >= -18:
        print(pos_str)
        cam = PiCamera(sensor_mode=1, resolution=(1920, 1080))
        cam.annotate_text = pos_str
        cam.annotate_text_size = 20
        sleep(2)
        res_file = (Path(r'/mnt/nas/') / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_chives.jpg')
        cam.capture(res_file.as_posix())
        print(f'Captured to {res_file.name}')
        cam.close()
    else:
        print(f'Skipping, {pos_str}')
