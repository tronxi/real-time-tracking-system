import json
import matplotlib.pyplot as plt
from datetime import datetime

filename = 'altitude_20250628_025855.jsonl'

timestamps = []
altitudes = []
pressures = []
temperatures = []
cpu_temperatures = []

with open(filename, 'r') as file:
    for line in file:
        try:
            data = json.loads(line)
            dt = datetime.fromisoformat(data["datetime"])
            payload = data["payload"]

            timestamps.append(dt)
            altitudes.append(payload["altitude"])
            pressures.append(payload["pressure"])
            temperatures.append(payload["temperature"])
            cpu_temperatures.append(payload["cpuTemperature"])
        except (json.JSONDecodeError, KeyError):
            continue

plt.figure(figsize=(12, 6))
plt.plot(timestamps, altitudes, label='Altitude (m)')
plt.plot(timestamps, pressures, label='Pressure (hPa)')
plt.plot(timestamps, temperatures, label='Temp (°C)')
plt.plot(timestamps, cpu_temperatures, label='CPU Temp (°C)')

plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Telemetry Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
