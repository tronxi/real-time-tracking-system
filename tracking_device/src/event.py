import json


class Event:

    def __init__(self, event_type, datetime, payload=None):
        self.type = event_type
        self.datetime = datetime
        self.payload = payload

    def to_json(self):
        return json.dumps(self.__dict__, default=str)
