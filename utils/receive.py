import time
from datetime import datetime, timedelta

import RPi.GPIO as GPIO
import pandas as pd


def scan(scan_time: float, sleep: float = None) -> pd.Series:
    RECEIVE_PIN = 11
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=scan_time)

    x, y = [], []
    print('Scanning...')
    while (current_time := datetime.now()) <= end_time:
        y.append(GPIO.input(RECEIVE_PIN))
        x.append(current_time - start_time)
        if sleep is not None:
            time.sleep(sleep)
    print(f'{len(x)} samples')
    return pd.Series(y, index=pd.TimedeltaIndex(x))


if __name__ == '__main__':
    scan(5.0)