import logging, traceback, time
from threading import Event
from enum import Enum

class Pipeline:
    sample_event = Event()
    spectrum = []
    signal = []
    def __init__(self):
        self.sample = None
        self.exit_flag = False
        try:
            self.exit_flag = False
        except Exception as e:
            logging.exception(traceback.format_exc())

    def emit(self, signal, spectrum):
        self.signal = signal
        self.spectrum = spectrum
        self.sample_event.set()

    def consume(self):
        start = time.time()
        self.sample_event.clear()
        self.sample_event.wait()
        print(time.time() - start, self.signal)
        return self.signal
    
    def check(self):
        return self.sample != None

    def set_exit(self, flag):
        self.exit_flag = True

    def should_exit(self):
        return self.exit_flag

pipeline = Pipeline()
