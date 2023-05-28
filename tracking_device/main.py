import sys
import camera
import heartbeat_sender as hs
import signal
import serial_port_reader
from threading import Thread


class Main:
    def __init__(self):
        self.cam = None
        self.spr = None
        self.thread_cam = Thread(target=self.start_cam)
        self.thread_heartbeat_sender = Thread(target=self.start_heartbeat_sender)
        self.thread_serial_port_reader = Thread(target=self.start_serial_port_reader)
        signal.signal(signal.SIGINT, self.exit_program)
        signal.signal(signal.SIGTSTP, self.exit_program)

    def start_cam(self):
        self.cam = camera.Camera()
        self.cam.start()

    def start_serial_port_reader(self):
        self.spr = serial_port_reader.SerialPortReader()
        self.spr.start()

    def start_heartbeat_sender(self):
        heartbeat_sender = hs.HeartbeatSender()
        heartbeat_sender.start()

    def exit_program(self, signum, frame):
        if self.cam is not None:
            self.cam.close()
        if self.spr is not None:
            self.spr.close()
        exit(1)

    def main(self, args):
        if args == "all":
            self.thread_cam.start()
            self.thread_heartbeat_sender.start()
            self.thread_serial_port_reader.start()
        elif args == "cam":
            self.thread_cam.start()
        elif args == "serial":
            self.thread_serial_port_reader.start()
        elif args == "heart":
            self.thread_heartbeat_sender.start()


if __name__ == "__main__":
    arg = "all"
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    Main().main(arg)
