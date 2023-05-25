import cv2
from picamera2 import Picamera2
import subprocess
import signal

width = 640
height = 480
rtmp_url = "rtmp://tronxi.ddns.net:1935/live/test"
picam2 = Picamera2()
picam2.preview_configuration.main.size = (width, height)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

def handler(signum, frame):
  picam2.close()
  exit(1)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTSTP, handler)

command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', "20",
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmp_url]

p = subprocess.Popen(command, stdin=subprocess.PIPE)
while True:
	im = picam2.capture_array()
	p.stdin.write(im.tobytes())