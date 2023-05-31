import time
import event
from datetime import datetime


class HeartbeatSender:

    def __init__(self, rabbitmq_connection_manager, channel):
        self._rabbitmq_connection_manager = rabbitmq_connection_manager
        self._channel = channel

    def start(self):
        while True:
            ev = event.Event("HEARTBEAT", datetime.now())
            self._rabbitmq_connection_manager.publish(self._channel, ev.to_json())
            print(ev.to_json())
            time.sleep(5)
