import time
import event
from datetime import datetime


class HeartbeatSender:

    def __init__(self):
        self._url = "url"

    def start(self):
        while True:
            ev = event.Event("HEARTBEAT", datetime.now())
            print(ev.to_json())
            time.sleep(5)
