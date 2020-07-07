import time, os, sys, traceback
import threading
import concurrent.futures
import logging
import signal
import matplotlib.pyplot as plt

from database import Database
from sample import Sample
from fft import FFT
from pipeline import pipeline

plt.ion()

def sig_handler(signal, frame):
    global pipeline
    pipeline.set_exit(True)
    sys.exit()

if __name__ == '__main__':
    global pipeline
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    sample = Sample()
    fft = FFT()
    database = Database()
    signal.signal(signal.SIGINT, sig_handler)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(sample.run, pipeline)
        executor.submit(fft.run, pipeline)
        executor.submit(database.run, pipeline)
        while True:
            time.sleep(0.1)
