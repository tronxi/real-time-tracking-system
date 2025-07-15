import sys
try:
    import camera
except ImportError:
    pass
import signal
import telemetry_reader
import rabbitmq_connection_manager
import socket
import time
from datetime import datetime
from threading import Thread
from pathlib import Path
from lora_sender import LoraSender


class Main:
    def __init__(self):
        self.internet = self.wait_for_internet(timeout=120)
        self.current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = Path.home() / self.current_date
        filepath.mkdir(parents=True, exist_ok=True)
        self.connection_manager_telemetry = rabbitmq_connection_manager.RabbitmqConnectionManager()
        self.lora_sender = LoraSender()
        self.cam = None
        self.tmr = None
        if self.internet:
            self.thread_cam = Thread(target=self.start_cam)
        self.thread_telemetry_reader = Thread(
            target=self.start_telemetry_reader
        )
        signal.signal(signal.SIGINT, self.exit_program)
        signal.signal(signal.SIGTSTP, self.exit_program)

    def start_cam(self):
        self.cam = camera.Camera(self.current_date)
        self.cam.start()

    def start_telemetry_reader(self):
        self.tmr = telemetry_reader.TelemetryReader(self.connection_manager_telemetry, self.current_date, self.lora_sender, False)
        self.tmr.start()

    def exit_program(self, signum, frame):
        if self.cam is not None:
            self.cam.close()
        if self.tmr is not None:
            self.tmr.close()
        self.connection_manager_telemetry.close()
        self.lora_sender.close()
        exit(1)

    def main(self, args):
        if args == "all":
            self.thread_cam.start()
            self.thread_telemetry_reader.start()
        elif args == "cam":
            self.thread_cam.start()
        elif args == "tm":
            self.thread_telemetry_reader.start()

    def wait_for_internet(self, timeout=30):
        print("Waiting for internet connection...")
        start = time.time()
        while time.time() - start < timeout:
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                print("Internet connection detected.")
                return True
            except OSError:
                print("No internet yet, retrying...")
                time.sleep(5)
        print("Warning: No internet connection after timeout.")
        return False



if __name__ == "__main__":
    arg = "all"
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    Main().main(arg)
