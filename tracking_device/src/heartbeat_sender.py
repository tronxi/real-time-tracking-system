import time


class HeartbeatSender:

    def __init__(self):
        self._url = "url"

    def start(self):
        while True:
            print("sending to url" + self._url)
            time.sleep(5)
