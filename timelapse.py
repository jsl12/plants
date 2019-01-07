from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta

class Timelapse:
    def __init__(self, **kwargs):
        self.period = timedelta(**kwargs)
        self.cam = PiCamera()
        self.cam.resolution = (1920, 1080)
        self.cam.vflip = True
        sleep(2)

    def run(self):
        for filename in self.cam.capture_continuous('images/{timestamp:%Y-%m-%d_%H%M%S}_img.jpg'):
            print(filename)
            self.last_run = datetime.now()
            self.wait()

    def wait(self):
        wt = (self.last_run + self.period) - datetime.now()
        sleep(wt.total_seconds())

if __name__ == '__main__':
    t = Timelapse(minutes=1)
    t.run()