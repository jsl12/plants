import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd

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
    return next(Path(w1_device_folder).glob('28*')) / 'w1_slave'


def read_lines() -> List[str]:
    with device().open('r') as file:
        return file.readlines()


def read_temp() -> float:
    while (lines := read_lines())[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
    if (pos := lines[1].find('t=')) != -1:
        return float(lines[1][pos+2:]) / 1000


def sql_conn(db_file)-> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    else:
        return conn


def record_temp(db_file: str, table_name: str = 'temp_readings'):
    conn = sql_conn(db_file)
    try:
        with conn:
            create_table_command = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                        time datetime PRIMARY KEY,
                                        temp real NOT NULL
                                    );"""
            conn.execute(create_table_command)

            insert_value_command = f'INSERT INTO {table_name}(time,temp) VALUES(?,?);'
            conn.execute(insert_value_command, (datetime.now(), read_temp()))
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()


def read_temp_df(db_file: Path, table_name: str = 'temp_readings') -> pd.DataFrame:
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql(f'select * from {table_name}', conn, index_col='time', parse_dates='time')
    conn.close()
    return df


if __name__ == '__main__':
    print(f'{read_temp():.1f} C')
    p = Path('/home/pi/Documents/plants/temps.db')
    record_temp(p)
    df = read_temp_df(p)
    print(df.iloc[-5:])
