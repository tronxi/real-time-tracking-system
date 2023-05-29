import serial
import json

class SerialPortReader:

    def __init__(self):
        self.port = serial.Serial('/dev/ttyUSB0', 9600)

    def close(self):
        self.port.close()

    def start(self):
        while True:
            line = self.port.readline().decode()
            serial_event = json.loads(line)
            print(line)
            print(serial_event["type"])
