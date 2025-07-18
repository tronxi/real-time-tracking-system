from picamera2 import Picamera2
import subprocess
import cv2
from pathlib import Path

class Camera:

    def __init__(self, current_date, send_online):
        self._send_online = send_online
        self._width = 640
        self._height = 480
        self._framerate = 15
        self._rtmp_url = "rtmp://tronxi.ddns.net:1935/live/test"
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        filename = f"video_{current_date}.avi"
        filepath = Path.home() / current_date / filename
        self.out = cv2.VideoWriter(str(filepath), fourcc, self._framerate, (self._width, self._height))

        self._picam2 = Picamera2()
        config = self._picam2.create_video_configuration(
            main={"size": (self._width, self._height), "format": "RGB888"},
            controls={"FrameDurationLimits": (int(1e6 / self._framerate), int(1e6 / self._framerate))}
        )
        self._picam2.configure(config)

        self._ffmpeg_cmd = [
            'ffmpeg',
            '-fflags', 'nobuffer',
            '-f', 'rawvideo',
            '-pix_fmt', 'rgb24',
            '-s', f'{self._width}x{self._height}',
            '-r', str(self._framerate),
            '-i', '-',
            '-c:v', 'h264_v4l2m2m',
            '-pix_fmt', 'yuv420p',
            '-f', 'flv',
            self._rtmp_url
        ]

    def close(self):
        self._picam2.close()

    def start(self):
        self._picam2.start()
        if self._send_online:
            ffmpeg = subprocess.Popen(self._ffmpeg_cmd, stdin=subprocess.PIPE)
        else: ffmpeg = None
        try:
            while True:
                frame = self._picam2.capture_array("main")
                if ffmpeg and ffmpeg.stdin:
                    ffmpeg.stdin.write(frame.tobytes())
                self.out.write(frame)
        except BrokenPipeError:
            print("FFmpeg pipe broken.")
        finally:
            self._picam2.stop()
            self.out.release()
            if ffmpeg:
                if ffmpeg.stdin:
                    ffmpeg.stdin.close()
                ffmpeg.wait()
