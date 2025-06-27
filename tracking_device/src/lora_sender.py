import serial
import time
import RPi.GPIO as GPIO


class LoraSender:

    def __init__(self):
        self.M0 = 23
        self.M1 = 24

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup((self.M0, self.M1), GPIO.OUT, initial=GPIO.LOW)

        self.ser = serial.Serial('/dev/serial0', 9600)

    def send(self, body):
        self.ser.write((body + '\n').encode())
        time.sleep(0.3)

    def close(self):
        self.ser.close()
