from datetime import datetime
import serial
import time
import os
import rabbitmq_connection_manager
import event as event_module
import json

PORT = '/dev/cu.usbserial-0001'
rabbit = rabbitmq_connection_manager.RabbitmqConnectionManager()

print("Checking port access...")
if os.path.exists(PORT) and os.access(PORT, os.R_OK | os.W_OK):
    print("Port exists and is accessible, trying to open...")
    try:
        ser = serial.Serial(PORT, 115200, timeout=1)
        print("Serial port opened.")

        print("Reading data (Ctrl+C to stop)...")
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                try:
                    payload = json.loads(line)
                except Exception:
                    payload = {"raw": line}

                event = event_module.Event("TM", datetime.now().isoformat(), payload)
                print(f"Received: {event.to_json()}")
                rabbit.publish(event.to_json())
            time.sleep(0.1)

    except Exception as e:
        print(f"Error opening port: {e}")
else:
    print(f"Port {PORT} not accessible or doesn't exist.")
