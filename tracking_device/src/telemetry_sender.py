import time
import event
import math
from datetime import datetime
from pathlib import Path
from event_logger import EventLogger
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ROTATION_VECTOR
import board
import busio
import adafruit_bmp3xx
from gpiozero import CPUTemperature
import serial
import pynmea2

class TelemetrySender:

    def __init__(self, rabbitmq_connection_manager, current_date, lora_sender, send_online):
        filename = f"telemetry_{current_date}.jsonl"
        filepath = Path.home() / current_date / filename

        self._send_online = send_online
        self.logger = EventLogger(str(filepath))
        self._rabbitmq_connection_manager = rabbitmq_connection_manager
        self._lora_sender = lora_sender
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c, address=0x77)
        self._base_altitude = None
        self._last_altitude_data = {}
        self._port = serial.Serial('/dev/ttyUSB0', 9600)
        self._last_position_data = {}
        self._last_lora_send = 0
        self._bno = BNO08X_I2C(i2c)
        self._bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

    def start(self):
        while True:
            try:
                current_altitude = self.bmp.altitude
                if self._base_altitude is None:
                    self._base_altitude = current_altitude
                self._last_altitude_data["altitude"] = round(current_altitude - self._base_altitude, 2)
                self._last_altitude_data["pressure"] = round(self.bmp.pressure, 2)
                self._last_altitude_data["temperature"] = round(self.bmp.temperature, 2)
                self._last_altitude_data["cpuTemperature"] = round(CPUTemperature().temperature, 2)

                line = self._port.readline().decode(errors='replace').strip()
                if line.startswith("$GNGGA") or line.startswith("$GPGGA"):
                    msg = pynmea2.parse(line)
                    self._last_position_data["hdop"] = float(msg.horizontal_dil) if msg.horizontal_dil is not None else None
                    self._last_position_data["satellites"] = int(msg.num_sats) if msg.num_sats is not None else None
                    self._last_position_data["altitude"] = float(msg.altitude) if msg.altitude is not None else None


                elif line.startswith("$GNRMC") or line.startswith("$GPRMC"):
                    msg = pynmea2.parse(line)
                    if msg.status == 'A':
                        self._last_position_data["lat"] = msg.latitude
                        self._last_position_data["long"] = msg.longitude
                        self._last_position_data["speed"] = float(msg.spd_over_grnd) * 1.852 if msg.spd_over_grnd is not None else None

                try:
                    quat = self._bno.quaternion
                    if quat:
                        pitch, roll, yaw = self._quaternion_to_euler(quat)
                        self._last_position_data["roll"] = roll
                        self._last_position_data["pitch"] = pitch
                        self._last_position_data["yaw"] = yaw
                    else:
                        print("No quaternion data")
                except Exception as e:
                    print(f"[WARNING] BNO085 error: {e}")
                    i2c = busio.I2C(board.SCL, board.SDA)
                    self._bno = BNO08X_I2C(i2c)
                    self._bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

                self._publish_telemetry_event()
            except pynmea2.ParseError:
                continue
            except Exception as e:
                print(f"[ERROR] {e}")
            time.sleep(0.5)

    def _publish_telemetry_event(self):
        payload = {
            "altitude": self._last_altitude_data.get("altitude"),
            "pressure": self._last_altitude_data.get("pressure"),
            "temperature": self._last_altitude_data.get("temperature"),
            "cpuTemperature": self._last_altitude_data.get("cpuTemperature"),
            "lat": self._last_position_data.get("lat"),
            "long": self._last_position_data.get("long"),
            "gps_altitude": self._last_position_data.get("altitude"),
            "speed": self._last_position_data.get("speed"),
            "yaw": self._last_position_data.get("yaw"),
            "roll": self._last_position_data.get("roll"),
            "pitch": self._last_position_data.get("pitch"),
        }

        ev = event.Event("TM", datetime.now().isoformat(), payload)
        if self._send_online:
            self._rabbitmq_connection_manager.publish(event.Event.from_csv(ev.to_csv()).to_json())
        else:
            now = time.time()
            send_lora = (now - self._last_lora_send) >= 2.0
            if send_lora:
                self._last_lora_send = now
                self._lora_sender.send(ev)
        self.logger.log(ev)

    def _quaternion_to_euler(self, q):
        w, x, y, z = q
        sinr_cosp = 2.0 * (w * x + y * z)
        cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2.0 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return (
            math.degrees(pitch),
            math.degrees(roll),
            math.degrees(yaw)
        )

    def close(self):
        self._port.close()
