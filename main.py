import subprocess
from pathlib import Path

from utils.file import convert_filename

if __name__ == '__main__':
    args = [
        'raspistill',
        f'-o /mnt/nas/image_%010d.jpg',
        '-ts',
        '-n',
        '--mode 2',
        '-hf',
        '-vf'
    ]
    subprocess.run(args, shell=True)
    for file in Path(r'/mnt/nas/').glob('image*.jpg'):
        convert_filename(file, 'chives')
