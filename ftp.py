import ftplib
import re
from datetime import datetime
from pathlib import Path

IP = '192.168.1.126'
USER = 'pi'
PASSWORD = 'raspberry'

def get_pictures(result_folder=None, regex='\.(jpg|png)$', remove=False):
    if result_folder is None:
        result_folder = Path.cwd() / 'images'
    if not result_folder.exists():
        result_folder.mkdir(parents=True)

    regex = re.compile(regex)
    with ftplib.FTP(IP, USER, PASSWORD) as conn:
        conn.cwd('/home/pi/Pictures/plants/')
        files = [f for f in conn.mlsd() if regex.search(f[0]) is not None]
        files = sorted(files)
        for f in files:
            if match := re.compile('image_(\d+)\.jpg').search(f[0]):
                date = datetime.fromtimestamp(int(match.group(1)))
                res_file = result_folder / f'{date.strftime("%Y-%m-%d_%H.%M.%S")}_plants.jpg'
            else:
                res_file = result_folder / f[0]
            if not res_file.exists():
                with open(res_file, 'wb') as file:
                    conn.retrbinary(f'RETR {f[0]}', file.write)
                    if remove:
                        conn.delete(f[0])
                    print(res_file.name)
            elif remove:
                conn.delete(f[0])

def send_file(file):
    with ftplib.FTP(IP, USER, PASSWORD) as conn:
        conn.storbinary('STOR {}'.format(file.name), open(file, 'rb'))

if __name__ == '__main__':
    get_pictures()
