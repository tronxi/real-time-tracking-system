import serial
import time
import RPi.GPIO as GPIO

M0 = 23
M1 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup((M0, M1), GPIO.OUT, initial=GPIO.LOW)

ser = serial.Serial('/dev/serial0', 9600)
time.sleep(0.2)

print("Escribe un mensaje para enviar por LoRa. Ctrl+C para salir.")

try:
    while True:
        msg = input("> ")
        ser.write((msg + '\n').encode())
        time.sleep(0.3)
except KeyboardInterrupt:
    print("\nSalida por el usuario.")
finally:
    ser.close()
