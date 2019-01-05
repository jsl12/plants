from time import sleep
from picamera import PiCamera
import click

@click.command()
@click.option('--filename', '-f', type=str, default='foo.jpg')
def take_picture(filename):
    camera = PiCamera()
    camera.resolution = (1920, 1080)
    sleep(2)
    camera.vflip = True
    camera.capture(filename)
    print('Done')

if __name__ == '__main__':
    take_picture()