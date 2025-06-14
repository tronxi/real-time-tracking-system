from picamera2 import Picamera2
import subprocess

class Camera:

    def __init__(self):
        self._width = 640     # Más pequeño = menos latencia
        self._height = 480
        self._framerate = 25  # Menor FPS = menos datos a transmitir
        self._rtmp_url = "rtmp://tronxi.ddns.net:1935/live/test"

        self._picam2 = Picamera2()
        config = self._picam2.create_video_configuration(
            main={"size": (self._width, self._height), "format": "YUV420"},
            controls={"FrameDurationLimits": (int(1e6 / self._framerate), int(1e6 / self._framerate))}
        )
        self._picam2.configure(config)

        self._ffmpeg_cmd = [
            'ffmpeg',
            '-f', 'rawvideo',
            '-pix_fmt', 'yuv420p',
            '-s', f'{self._width}x{self._height}',
            '-r', str(self._framerate),
            '-i', '-',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-f', 'flv',
            self._rtmp_url
        ]

    def close(self):
        self._picam2.close()

    def start(self):
        self._picam2.start()
        ffmpeg = subprocess.Popen(self._ffmpeg_cmd, stdin=subprocess.PIPE)
        try:
            while True:
                frame = self._picam2.capture_array("main")
                if ffmpeg.stdin:
                    ffmpeg.stdin.write(frame.tobytes())
        except BrokenPipeError:
            print("FFmpeg pipe broken.")
        finally:
            self._picam2.stop()
            if ffmpeg.stdin:
                ffmpeg.stdin.close()
            ffmpeg.wait()
