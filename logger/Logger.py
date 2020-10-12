import sys
from datetime import datetime, timedelta


class Logger:
    def __init__(self, filename: str):
        self.terminal = sys.stdout
        self.filename = filename
        self.log = open(filename, "w")
        self.log.write("")
        self._save()

    def write(self, message: str):
        self.terminal.write(message)
        self.log.write(message)

        if self.lastSaveTime + timedelta(minutes=1) < datetime.now():
            self._save()


    def flush(self):
        pass

    def _save(self):
        self.log.close()
        self.log = open(self.filename, "a")
        self.lastSaveTime = datetime.now()
