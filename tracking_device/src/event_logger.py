class EventLogger:

    def __init__(self, filepath):
        self.filepath = filepath

    def log(self, event):
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(event.to_json() + '\n')