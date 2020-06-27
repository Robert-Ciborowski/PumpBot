"""
Stalls a thread while allowing other functions to be run from the thread.
Normally, I would just use more threads, but I can only use 2 threads, so
a bunch of update() functions must be run using this function rather than on
their own thread. Why only use 2 threads? Because Python is garbage and running
more than 2 threads makes TensorFlow predictions slower (by a magnitude of 80
on my PC).
"""

from datetime import datetime
from typing import List
import threading as th

class ThreadRunner:
    endTime: datetime
    _functionsToRun: List
    _functionsToRunLock: th.Lock
    _resultLock: th.Lock
    _functionsToRunPeriodically: List
    _functionsToRunPeriodicallyLock: th.Lock

    def __init__(self, endTime=None):
        self.endTime = endTime
        self._functionsToRun = []
        self._functionsToRunPeriodically = []
        self._result = None
        self._functionsToRunLock = th.Lock()
        self._functionsToRunPeriodicallyLock = th.Lock()
        self._resultLock = th.Lock()

    def start(self):
        if self.endTime is None:
            while True:
                self._update()
        else:
            while datetime.now() < self.endTime:
                self._update()

    def _update(self):
        with self._functionsToRunLock:
            if len(self._functionsToRun) != 0:
                self._result = self._functionsToRun.pop()()

        with self._functionsToRunPeriodicallyLock:
            for f in self._functionsToRunPeriodically:
                f()


    def run(self, function):
        with self._resultLock:
            with self._functionsToRunLock:
                self._functionsToRun.append(function)

            # Allow start() to access functionsToRun

            with self._functionsToRunLock:
                result = self._result
                print("ThreadRunner: " + str(result))
                self._result = None

            return result

    def runPerdiodically(self, function):
        with self._functionsToRunPeriodicallyLock:
            self._functionsToRunPeriodically.append(function)
