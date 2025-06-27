import sys
try:
    import camera
except ImportError:
    pass
import heartbeat_sender as hs
import signal
import gps_reader
import rabbitmq_connection_manager
import socket
import time
from datetime import datetime
from threading import Thread
from pathlib import Path
from lora_sender import LoraSender


class Main:
    def __init__(self):
        self.wait_for_internet(timeout=120)
        self.current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = Path.home() / self.current_date
        filepath.mkdir(parents=True, exist_ok=True)
        self.connection_manager_heart = rabbitmq_connection_manager.RabbitmqConnectionManager()
        self.connection_manager_gps = rabbitmq_connection_manager.RabbitmqConnectionManager()
        self.lora_sender = LoraSender()
        self.cam = None
        self.spr = None
        self.thread_cam = Thread(target=self.start_cam)
        self.thread_heartbeat_sender = Thread(
            target=self.start_heartbeat_sender)
        self.thread_gps_reader = Thread(
            target=self.start_gps_reader)
        signal.signal(signal.SIGINT, self.exit_program)
        signal.signal(signal.SIGTSTP, self.exit_program)

    def start_cam(self):
        self.cam = camera.Camera(self.current_date)
        self.cam.start()

    def start_gps_reader(self):
        self.spr = gps_reader.GPSReader(self.connection_manager_gps, self.current_date, self.lora_sender)
        self.spr.start()

    def start_heartbeat_sender(self):
        heartbeat_sender = hs.HeartbeatSender(self.connection_manager_heart, self.current_date, self.lora_sender)
        heartbeat_sender.start()

    def exit_program(self, signum, frame):
        if self.cam is not None:
            self.cam.close()
        if self.spr is not None:
            self.spr.close()
        self.connection_manager_heart.close()
        self.connection_manager_gps.close()
        exit(1)

    def main(self, args):
        if args == "all":
            self.thread_cam.start()
            self.thread_heartbeat_sender.start()
            self.thread_gps_reader.start()
        elif args == "cam":
            self.thread_cam.start()
        elif args == "gps":
            self.thread_gps_reader.start()
        elif args == "heart":
            self.thread_heartbeat_sender.start()

    def wait_for_internet(self, timeout=120):
        print("Waiting for internet connection...")
        start = time.time()
        while time.time() - start < timeout:
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                print("Internet connection detected.")
                return
            except OSError:
                print("No internet yet, retrying...")
                time.sleep(5)
        print("Warning: No internet connection after timeout.")



if __name__ == "__main__":
    arg = "all"
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    Main().main(arg)
