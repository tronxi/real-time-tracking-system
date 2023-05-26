import camera
import signal
from threading import Thread

cam = camera.Camera()


def start_cam():
    cam.start()


thread_cam = Thread(target=start_cam)


def exit_program(signum, frame):
    cam.close()
    exit(1)


signal.signal(signal.SIGINT, exit_program)
signal.signal(signal.SIGTSTP, exit_program)


def main():
    thread_cam.start()
    print("otra cosa")


if __name__ == "__main__":
    main()
