import serial
import time
import json
import RPi.GPIO as GPIO
import rabbitmq_connection_manager

M0, M1 = 23, 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup((M0, M1), GPIO.OUT, initial=GPIO.LOW)

rabbit = rabbitmq_connection_manager.RabbitmqConnectionManager()
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

buffer = ""

try:
    while True:
        data = ser.read(ser.in_waiting or 1).decode('utf-8', errors='ignore')
        buffer += data

        while '$' in buffer:
            message, buffer = buffer.split('$', 1)
            message = message.strip()
            if not message:
                continue
            try:
                parsed = json.loads(message)
                print("✅ JSON recibido:", parsed)
                rabbit.publish(message)
                ser.write(b'OK\n')
            except json.JSONDecodeError:
                print("❌ JSON malformado:", repr(message))

except KeyboardInterrupt:
    pass
finally:
    ser.close()
    rabbit.close()
