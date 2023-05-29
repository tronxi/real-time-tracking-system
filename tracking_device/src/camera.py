from picamera2 import Picamera2
import subprocess


class Camera:

    def __init__(self):
        self._picam2 = Picamera2()
        self._width = 1280
        self._height = 720
        self._rtmp_url = "rtmp://tronxi.ddns.net:1935/live/test"
        self._picam2.preview_configuration.main.size = (
            self._width, self._height)
        self._picam2.preview_configuration.main.format = "RGB888"
        self._picam2.preview_configuration.align()
        self._picam2.configure("preview")
        self._command = ['ffmpeg',
                         '-y',
                         '-f', 'rawvideo',
                         '-vcodec', 'rawvideo',
                         '-pix_fmt', 'bgr24',
                         '-s', "{}x{}".format(self._width, self._height),
                         '-r', "30",
                         '-i', '-',
                         '-c:v', 'libx264',
                         '-pix_fmt', 'yuv420p',
                         '-preset', 'ultrafast',
                         '-f', 'flv',
                         self._rtmp_url]

    def close(self):
        self._picam2.close()

    def start(self):
        self._picam2.start()
        p = subprocess.Popen(self._command, stdin=subprocess.PIPE)
        while True:
            im = self._picam2.capture_array()
            p.stdin.write(im.tobytes())
