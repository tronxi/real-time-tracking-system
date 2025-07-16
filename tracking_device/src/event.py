import json
import csv
from io import StringIO

class Event:

    ALL_FIELDS = ['lat', 'long', 'gps_altitude', 'altitude', 'speed', 'roll', 'pitch', 'yaw', 'pressure', 'temperature', 'cpuTemperature', 'yaw']


    def __init__(self, event_type, datetime, payload=None):
        self.type = event_type
        self.datetime = datetime
        self.payload = payload

    def to_json(self):
        return json.dumps(self.__dict__, default=str, separators=(',', ':'))

    def to_csv(self):
        output = StringIO()
        writer = csv.writer(output)
        row = [self.type, self.datetime]
        for field in self.ALL_FIELDS:
            value = self.payload.get(field, "")
            row.append("" if value is None else value)
        writer.writerow(row)
        return output.getvalue().strip()

    @classmethod
    def from_csv(cls, csv_string):
        input_stream = StringIO(csv_string)
        reader = csv.reader(input_stream)
        row = next(reader)
        event_type = row[0]
        datetime = row[1]
        payload_values = row[2:]
        payload = {}
        for key, value in zip(cls.ALL_FIELDS, payload_values):
            if value == "":
                continue
            try:
                payload[key] = float(value)
            except ValueError:
                payload[key] = value
        return cls(event_type, datetime, payload)
