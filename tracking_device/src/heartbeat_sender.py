import time
import event
from datetime import datetime
from gpiozero import CPUTemperature


class HeartbeatSender:

    def __init__(self, rabbitmq_connection_manager):
        self._rabbitmq_connection_manager = rabbitmq_connection_manager

    def start(self):
        while True:
            cpu = CPUTemperature()
            payload = {
                "cpuTemperature": cpu.temperature
            }
            ev = event.Event("HEARTBEAT", datetime.now(), payload)
            self._rabbitmq_connection_manager.publish(ev.to_json())
            time.sleep(5)
