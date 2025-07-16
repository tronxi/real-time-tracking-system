from picamera2 import Picamera2
from pathlib import Path
import cv2

class CameraOffline:
    def __init__(self, current_date):
        self.filename = f"video_{current_date}.avi"
        self.folder = Path.home() / current_date
        self.filepath = str(self.folder / self.filename)

        self._width = 1920
        self._height = 1080
        self._framerate = 30

        self.picam2 = Picamera2()
        self.config = self.picam2.create_video_configuration(
            main={"size": (self._width, self._height), "format": "RGB888"},
            controls={"FrameDurationLimits": (int(1e6 / self._framerate), int(1e6 / self._framerate))}
        )
        self.picam2.configure(self.config)

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter(self.filepath, fourcc, self._framerate, (self._width, self._height))

    def start(self):
        self.picam2.start()
        try:
            while True:
                frame = self.picam2.capture_array()
                self.out.write(frame)
        except KeyboardInterrupt:
            print("Stopping offline camera...")
        finally:
            self.close()

    def close(self):
        self.picam2.stop()
        self.out.release()
        self.picam2.close()