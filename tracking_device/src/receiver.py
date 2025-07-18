import serial
import time
import RPi.GPIO as GPIO
import rabbitmq_connection_manager
import event as event_module
import os
import socket

M0, M1 = 23, 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup((M0, M1), GPIO.OUT, initial=GPIO.LOW)

print("Waiting for internet connection...")
start = time.time()
internet_connected = False

while time.time() - start < 30:
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("Internet connection detected.")
        internet_connected = True
        break
    except OSError:
        print("No internet yet, retrying...")
        time.sleep(5)

if not internet_connected:
    print("Warning: No internet connection after timeout")
    exit(1)

rabbit = rabbitmq_connection_manager.RabbitmqConnectionManager()

print("Waiting for serial port to become available...")
start_time = time.time()
ser = None
PORT = '/dev/serial0'
while time.time() - start_time < 30:
    print("Checking port access...")
    if os.path.exists(PORT) and os.access(PORT, os.R_OK | os.W_OK):
        print("Port exists and is accessible, trying to open...")
        try:
            ser = serial.Serial(PORT, 9600, timeout=1)
            print("Serial port opened.")
            break
        except Exception as e:
            print(f"Error opening port: {e}")
    else:
        print(f"Port {PORT} not accessible or doesn't exist.")
    time.sleep(1)


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

