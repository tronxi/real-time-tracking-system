from picamera2 import Picamera2
import subprocess
import time
import numpy as np
import cv2

class Camera:

    def __init__(self):
        self._picam2 = Picamera2()
        self._width = 1280
        self._height = 720
        self._rtmp_url = "rtmp://tronxi.ddns.net:1935/live/test"

        config = self._picam2.create_preview_configuration(
            main={"size": (self._width, self._height), "format": "RGB888"}
        )
        self._picam2.configure(config)

        self._command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'rgb24',
            '-s', f"{self._width}x{self._height}",
            '-r', '30',
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'flv',
            self._rtmp_url
        ]

    def close(self):
        self._picam2.close()

    def start(self):
        self._picam2.start()
        try:
            p = subprocess.Popen(self._command, stdin=subprocess.PIPE)
            while True:
                im = self._picam2.capture_array()
                if p.stdin:
                    try:
                        p.stdin.write(im.tobytes())
                    except BrokenPipeError:
                        print("Error: ffmpeg")
                        break
                time.sleep(1 / 30.0)  # Control de FPS
        finally:
            self._picam2.stop()
            p.stdin.close()
            p.wait()
