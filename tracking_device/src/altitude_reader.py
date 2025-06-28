import time
import event
from datetime import datetime
from pathlib import Path
from event_logger import EventLogger
import board
import busio
import adafruit_bmp3xx
from gpiozero import CPUTemperature


class AltitudeReader:
    def __init__(self, rabbitmq_connection_manager, current_date, lora_sender):
        filename = f"altitude_{current_date}.jsonl"
        filepath = Path.home() / current_date / filename

        self.logger = EventLogger(str(filepath))
        self._rabbitmq_connection_manager = rabbitmq_connection_manager
        self._lora_sender = lora_sender
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c, address=0x77)
        self.bmp.sea_level_pressure = 1013.25
        self._last_altitude_data = {}

    def start(self):
        while True:
            try:
                self._last_altitude_data["altitude"] = round(self.bmp.altitude, 2)
                self._last_altitude_data["pressure"] = round(self.bmp.pressure, 2)
                self._last_altitude_data["temperature"] = round(self.bmp.temperature, 2)
                self._last_altitude_data["cpuTemperature"] = round(CPUTemperature().temperature, 2)
                self._publish_altitude_event()
            except Exception as e:
                print(f"Error BMP388: {e}")
            time.sleep(2)

    def _publish_altitude_event(self):
        payload = {
            "altitude": self._last_altitude_data.get("altitude"),
            "pressure": self._last_altitude_data.get("pressure"),
            "temperature": self._last_altitude_data.get("temperature"),
            "cpuTemperature": self._last_altitude_data.get("cpuTemperature")
        }

        ev = event.Event("ALTITUDE", datetime.now(), payload)
        self._lora_sender.send(ev.to_json())
        self._rabbitmq_connection_manager.publish(ev.to_json())
        self.logger.log(ev)
