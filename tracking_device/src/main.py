import sys
try:
    import camera
except ImportError:
    pass
import signal
import gps_reader
import altitude_reader as ar
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
        self.connection_manager_gps = rabbitmq_connection_manager.RabbitmqConnectionManager()
        self.connection_manager_altitude = rabbitmq_connection_manager.RabbitmqConnectionManager()
        self.lora_sender = LoraSender()
        self.cam = None
        self.spr = None
        self.tmr = None
        self.thread_cam = Thread(target=self.start_cam)
        self.thread_gps_reader = Thread(
            target=self.start_gps_reader)
        self.thread_altitude_reader = Thread(
            target=self.start_altitude_reader
        )
        self.thread_telemetry_reader = Thread(
            target=self.start_telemetry_reader
        )
        signal.signal(signal.SIGINT, self.exit_program)
        signal.signal(signal.SIGTSTP, self.exit_program)

    def start_cam(self):
        self.cam = camera.Camera(self.current_date)
        self.cam.start()

    def start_gps_reader(self):
        self.spr = gps_reader.GPSReader(self.connection_manager_gps, self.current_date, self.lora_sender)
        self.spr.start()

    def start_telemetry_reader(self):
        self.tmr = telemetry_reader.TelemetryReader(self.connection_manager_gps, self.current_date, self.lora_sender)
        self.tmr.start()

    def start_altitude_reader(self):
        altitude_reader = ar.AltitudeReader(self.connection_manager_altitude, self.current_date, self.lora_sender)
        altitude_reader.start()

    def exit_program(self, signum, frame):
        if self.cam is not None:
            self.cam.close()
        if self.spr is not None:
            self.spr.close()
        if self.tmr is not None:
            self.tmr.close()
        self.connection_manager_gps.close()
        self.connection_manager_altitude.close()
        self.lora_sender.close()
        exit(1)

    def main(self, args):
        if args == "all":
            self.thread_cam.start()
            # self.thread_gps_reader.start()
            # self.thread_altitude_reader.start()
            self.thread_telemetry_reader.start()
        elif args == "cam":
            self.thread_cam.start()
        elif args == "gps":
            self.thread_gps_reader.start()
        elif args == "altitude":
            self.thread_altitude_reader.start()

    def wait_for_internet(self, timeout=120):
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
