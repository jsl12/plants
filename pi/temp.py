import logging
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)

"""
https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_1-Wire_DS18B20_Sensor
https://pinout.xyz/pinout/1_wire
Add to
/boot/config.txt
dtoverlay=w1-gpio,gpiopin=4

https://www.raspberrypi.org/forums/viewtopic.php?t=35508
Add to
/etc/modules
w1-gpio
w1-therm
"""


def device(w1_device_folder: str = '/sys/bus/w1/devices/') -> Path:
    try:
        return next(Path(w1_device_folder).glob('28*')) / 'w1_slave'
    except StopIteration as e:
        LOGGER.info(f'No devices found with the glob 28*')


def read_lines() -> List[str]:
    with device().open('r') as file:
        return file.readlines()


def read_temp() -> float:
    while (lines := read_lines())[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
    if (pos := lines[1].find('t=')) != -1:
        return float(lines[1][pos+2:]) / 1000


def sql_conn(db_file: Path)-> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        LOGGER.exception(e)
    else:
        LOGGER.info(f'Connected to {db_file.as_posix()}')
        return conn


def read_temp_df(db_file: Path, table_name: str = 'temp_readings') -> pd.DataFrame:
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql(f'select * from {table_name}', conn, index_col='time', parse_dates='time')
    conn.close()
    return df


def record_temps(num_reads: int, timing: float, db_file: Path, table_name: str = 'temp_readings', create_table: bool = False):
    data = np.full(num_reads, 0.0)
    times = np.full(num_reads, datetime.now())
    lock = threading.Lock()

    def read(i):
        try:
            with lock:
                # data[i], times[i] = random.random(), datetime.now()
                data[i], times[i] = read_temp(), datetime.now()
        except Exception as e:
            LOGGER.exception(e)
        else:
            LOGGER.info(f'{times[i].strftime("%H:%M:%S")} {data[i]:.1f}')

    threads = [threading.Timer(i * timing, read, args=(i,)) for i in range(num_reads)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with lock:
        add_to_sql(db_file=db_file,
                   times=times,
                   data=data,
                   table_name=table_name,
                   create_table=create_table)


def add_to_sql(db_file: Path, times: np.array, data: np.array, table_name: str, create_table: bool = False):
    try:
        with sql_conn(db_file) as conn:
            if create_table:
                create_table_command = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                            time datetime PRIMARY KEY,
                                            temp real NOT NULL
                                        );"""
                conn.execute(create_table_command)
                LOGGER.info(f'CREATE TABLE IF NOT EXISTS {table_name}')

            conn.executemany(f'INSERT INTO {table_name}(time,temp) VALUES(?,?);', zip(times, data))
    except sqlite3.Error as e:
        raise e
    else:
        LOGGER.info(f'Added {times.shape[0]} readings, average: {data.mean():.1f}C')
    finally:
        conn.close()
        LOGGER.info(f'Closed connection to {db_file.as_posix()}')


if __name__ == '__main__':
    print('Starting')
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s [%(levelname)s] %(module)s: %(message)s')
    p = Path('/home/pi/Documents/plants/temps.db')
    record_temps(
        num_reads=30,
        timing=1.0,
        db_file=p,
        # db_file=Path(r'C:\Users\lanca\OneDrive\Documents\Software\Plants\temp\temps.db'),
        # table_name='test',
        # create_table=True
    )
    print('Done')
