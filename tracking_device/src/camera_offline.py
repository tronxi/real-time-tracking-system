from picamera2 import Picamera2
from pathlib import Path
from picamera2.encoders import H264Encoder

class CameraOffline:
    def __init__(self, current_date):
        self.filename = f"video_{current_date}.mkv"
        self.folder = Path.home() / current_date
        self.filepath = str(self.folder / self.filename)

        self.picam2 = Picamera2()
        self.config = self.picam2.create_video_configuration(
            main={"size": (1920, 1080)},
            controls={"FrameRate": 30}
        )
        self.picam2.configure(self.config)

    def start(self):
        self.picam2.start_recording(H264Encoder(), self.filepath)

    def close(self):
        self.picam2.stop_recording()
