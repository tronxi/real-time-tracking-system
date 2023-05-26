import camera
import signal

cam = camera.Camera()


def exit_program(signum, frame):
    cam.close()
    exit(1)


signal.signal(signal.SIGINT, exit_program)
signal.signal(signal.SIGTSTP, exit_program)


def main():
    cam.start()


if __name__ == "__main__":
    main()
