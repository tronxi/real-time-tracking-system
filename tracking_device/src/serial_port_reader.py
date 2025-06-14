import serial
import json
import event
import pynmea2
from datetime import datetime
from pathlib import Path
from event_logger import EventLogger


class SerialPortReader:

    def __init__(self, rabbitmq_connection_manager):
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"serial_{current_date}.jsonl"
        filepath = Path.home() / filename

        self.logger = EventLogger(str(filepath))
        self._rabbitmq_connection_manager = rabbitmq_connection_manager
        self._port = serial.Serial('/dev/serial0', 9600)
        self._last_position_data = {}

    def close(self):
        self._port.close()

    def start(self):
        try:
            while True:
                try:
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
                            self._publish_position_event()

                except pynmea2.ParseError:
                    continue
                except Exception as e:
                    print(f"[ERROR] {e}")

        except KeyboardInterrupt:
            print("Interrupción detectada, cerrando puerto serial...")
            self.close()

    def _publish_position_event(self):
        position_event = {
            "type": "POSITION",
            "satellites": self._last_position_data.get("satellites"),
            "hdop": self._last_position_data.get("hdop"),
            "lat": self._last_position_data.get("lat"),
            "long": self._last_position_data.get("long"),
            "altitude": self._last_position_data.get("altitude"),
            "speed": self._last_position_data.get("speed")
        }

        ev = event.Event("POSITION", datetime.now(), position_event)
        self._rabbitmq_connection_manager.publish(ev.to_json())
        self.logger.log(ev)
