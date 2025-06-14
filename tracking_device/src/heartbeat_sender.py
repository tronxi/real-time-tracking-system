import time
import event
from pathlib import Path
from datetime import datetime
from gpiozero import CPUTemperature
from event_logger import EventLogger


class HeartbeatSender:

    def __init__(self, rabbitmq_connection_manager):
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"heart_{current_date}.jsonl"
        filepath = Path.home() / filename

        self.logger = EventLogger(str(filepath))
        self.logger = EventLogger("event_log.jsonl")
        self._rabbitmq_connection_manager = rabbitmq_connection_manager

    def start(self):
        while True:
            cpu = CPUTemperature()
            payload = {
                "cpuTemperature": cpu.temperature
            }
            ev = event.Event("HEARTBEAT", datetime.now(), payload)
            self._rabbitmq_connection_manager.publish(ev.to_json())
            self.logger.log(ev)
            time.sleep(5)
