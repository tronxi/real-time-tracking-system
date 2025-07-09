import serial
import time
import json
import RPi.GPIO as GPIO
import rabbitmq_connection_manager
import event

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
                event = event.Event.from_csv(message)
                print("✅ Valid CSV event received:", event.to_json())
                rabbit.publish(event)
                ser.write(b'OK\n')
            except Exception as e:
                print("❌ Malformed CSV event:", repr(message), "| Error:", str(e))

except KeyboardInterrupt:
    pass
finally:
    ser.close()
    rabbit.close()
