import serial
import time
import RPi.GPIO as GPIO
import threading
from queue import Queue

class LoraSender:

    def __init__(self):
        self.M0 = 23
        self.M1 = 24

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup((self.M0, self.M1), GPIO.OUT, initial=GPIO.LOW)
        self.queue = Queue()
        self.running = True

        self.ser = serial.Serial('/dev/ttySC0', 9600)
        self.sender_thread = threading.Thread(target=self._sender_loop, daemon=True)
        self.sender_thread.start()

    def _sender_loop(self):
        while self.running:
            body = self.queue.get()
            try:
                self.ser.write((body + '$').encode())
                self.ser.flush()
                start = time.time()
                ack = ""
                while "OK" not in ack and time.time() - start < 2:
                    if self.ser.in_waiting > 0:
                        ack += self.ser.read(self.ser.in_waiting).decode(errors='ignore')
                    time.sleep(0.01)
                if "OK" not in ack:
                    print("Error sending:", ack)
            except Exception as e:
                print("Error sending:", e)

    def send(self, event):
        self.queue.put(event.to_csv())

    def close(self):
        self.running = False
        self.sender_thread.join(timeout=1)
        self.ser.close()
