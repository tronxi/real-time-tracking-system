import camera
import heartbeat_sender as hs
import signal
import serial_port_reader
from threading import Thread

cam = camera.Camera()
spr = serial_port_reader.SerialPortReader()


def start_cam():
    cam.start()


def start_serial_port_reader():
    spr.start()


def start_heartbeat_sender():
    heartbeat_sender = hs.HeartbeatSender()
    heartbeat_sender.start()


thread_cam = Thread(target=start_cam)
thread_heartbeat_sender = Thread(target=start_heartbeat_sender)
thread_serial_port_reader = Thread(target=start_serial_port_reader)


def exit_program(signum, frame):
    cam.close()
    spr.close()
    exit(1)


signal.signal(signal.SIGINT, exit_program)
signal.signal(signal.SIGTSTP, exit_program)


def main():
    thread_cam.start()
    thread_heartbeat_sender.start()
    thread_serial_port_reader.start()


if __name__ == "__main__":
    main()
