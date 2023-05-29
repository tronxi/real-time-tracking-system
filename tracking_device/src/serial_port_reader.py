import serial
import json
import event
from datetime import datetime


class SerialPortReader:

    def __init__(self):
        self.port = serial.Serial('/dev/ttyUSB0', 9600)

    def close(self):
        self.port.close()

    def start(self):
        while True:
            line = self.port.readline().decode()
            ev = self._create_event(line)
            print(ev.to_json())

    def _create_event(self, line):
        serial_event = json.loads(line)
        event_type = serial_event["type"]
        serial_event.pop("type")
        return event.Event(event_type, datetime.now(), serial_event)
