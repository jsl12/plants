from time import sleep
from picamera import PiCamera
from datetime import datetime
import click

@click.command()
@click.option('--filename', '-f', type=str, default='foo.jpg')
@click.option('--timestamp', type=bool, default=False)
def take_picture(filename, timestamp):
    if timestamp:
        filename = '{}_{}'.format(datetime.now().strftime('%Y-%m-%d_%H%M'), filename)

    camera = PiCamera()
    camera.resolution = (1920, 1080)
    sleep(2)
    camera.vflip = True
    camera.capture(filename)
    print('Done')

if __name__ == '__main__':
    take_picture()