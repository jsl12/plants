import time
from pathlib import Path


def device(w1_device_folder: str = '/sys/bus/w1/devices/'):
    return next(Path(w1_device_folder).glob('28*')) / 'w1_slave'


def read_lines():
    with device().open('r') as file:
        return file.readlines()


def read_temp():
    while (lines := read_lines())[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
    if (pos := lines[1].find('t=')) != -1:
        return float(lines[1][pos+2:]) / 1000


if __name__ == '__main__':
    print(f'{read_temp()} C')
