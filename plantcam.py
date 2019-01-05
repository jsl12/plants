from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1920, 1080)
# camera.start_preview()
# Camera warm-up time
sleep(2)
camera.vflip = True
camera.capture('foo.jpg')
print('Done')