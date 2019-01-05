from pathlib import Path
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
            with open(result_folder / f[0], 'wb') as file:
                conn.retrbinary('RETR {}'.format(f[0]), file.write)

def send_file(file):
    with ftplib.FTP(IP, USER, PASSWORD) as conn:
        conn.storbinary('STOR {}'.format(file.name), open(file, 'rb'))

if __name__ == '__main__':
    get_pictures()
