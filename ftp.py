from pathlib import Path
from pprint import pprint
import ftplib
import re

IP = '192.168.1.126'
USER = 'pi'
PASSWORD = 'raspberry'

def get_pictures(result_folder=None, regex='\.(jpg|png)$'):
    if result_folder is None:
        result_folder = Path.cwd() / 'images'
    if not result_folder.exists():
        result_folder.mkdir(parents=True)

    regex = re.compile(regex)
    with ftplib.FTP(IP, USER, PASSWORD) as conn:
        files = [f for f in conn.mlsd() if regex.search(f[0]) is not None]
        for f in files:
            pprint(f)
            with open(result_folder / f[0], 'wb') as file:
                conn.retrbinary('RETR {}'.format(f[0]), file.write)

if __name__ == '__main__':
    get_pictures()
