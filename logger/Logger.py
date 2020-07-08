import sys

class Logger:
    def __init__(self, filename: str):
        self.terminal = sys.stdout
        self.log = open(filename, "w")
        self.log.write("")
        self.log.close()
        self.log = open(filename, "a")

    def write(self, message: str):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
