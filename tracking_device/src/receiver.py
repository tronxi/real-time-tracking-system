import serial
import time
import RPi.GPIO as GPIO
import rabbitmq_connection_manager
import event as event_module
import os

M0, M1 = 23, 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup((M0, M1), GPIO.OUT, initial=GPIO.LOW)

rabbit = rabbitmq_connection_manager.RabbitmqConnectionManager()

start_time = time.time()
ser = None
PORT = '/dev/serial0'
while time.time() - start_time < 30:
    if os.path.exists(PORT) and os.access(PORT, os.R_OK | os.W_OK):
        try:
            ser = serial.Serial(PORT, 9600, timeout=1)
            break
        except Exception:
            pass
    time.sleep(1)

if ser is None:
    print(f"Failed to open port {PORT} after {30} seconds")
    exit(1)
else:
    print(f"Opened port {PORT} successfully")

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
                event = event_module.Event.from_csv(message)
                json_event = event.to_json()
                rabbit.publish(json_event)
                # print("✅ Valid CSV event received:", json_event)
                ser.write(b'OK\n')
            except Exception as e:
                print("❌ Malformed CSV event:", repr(message), "| Error:", str(e))

except KeyboardInterrupt:
    pass
finally:
    ser.close()
    rabbit.close()
