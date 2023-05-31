import serial
import json
import event
from datetime import datetime


class SerialPortReader:

    def __init__(self, rabbitmq_connection_manager):
        self._rabbitmq_connection_manager = rabbitmq_connection_manager
        self._channel = self._rabbitmq_connection_manager.create_channel()
        self._port = serial.Serial('/dev/ttyUSB0', 9600)

    def close(self):
        self._port.close()

    def start(self):
        while True:
            line = self._port.readline().decode()
            ev = self._create_event(line)
            self._rabbitmq_connection_manager.publish(self._channel, ev.to_json())
            print(ev.to_json())

    def _create_event(self, line):
        serial_event = json.loads(line)
        event_type = serial_event["type"]
        serial_event.pop("type")
        return event.Event(event_type, datetime.now(), serial_event)
