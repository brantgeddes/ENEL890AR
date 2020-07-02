from message import decode_msg_size
import os, select, math, traceback, time, numpy as np
import sqlite3
from cmath import exp, pi, atan

# Target sample rate
sample_rate = 490
# Batch size
N = 8
# Queue Named Pipe
PIPE_NAME='ADC_READ_PIPE'

conn = sqlite3.connect('data.db')

def get_message(fifo: int) -> str:
    frame = os.read(fifo, 2)
    return 3.3 * int.from_bytes(frame, byteorder="big") / 2047

def fft(x):
    N = len(x)
    if N <= 1: return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [exp(-2j*pi*k/N)*odd[k] for k in range(N//2)]
    return [even[k] + T[k] for k in range(N//2)] + [even[k] - T[k] for k in range(N//2)]

def dft(batch):
    # Empty arrays
    real = np.array([])
    imag = np.array([])

    # Loop through all buckets
    for k in range(N):
        realV = 0
        imagV = 0
        # Perform a correlation for each bucket
        for n in range(N):
            realV += (1 / N) * batch[n] * math.cos(2 * math.pi * n * k / N)
            imagV += (1 / N) * batch[n] * math.sin(2 * math.pi * n * k / N)
        # Append correllation coefficients to the current bucket
        real = np.append(real, realV) 
        imag = np.append(imag, imagV)

    return (real, imag)

try:
    os.mkfifo(PIPE_NAME)
except:
    print("Pipe Exists")

try:
    fifo = os.open(PIPE_NAME, os.O_RDONLY)
except Exception as e:
    print(traceback.format_exc())
    exit()

try:
    batch = np.array([0]*N)
    i = 0
    while True:
        if fifo:
            new_value = get_message(fifo)
            batch = np.append(batch[1:], new_value)
            print(batch)
            """
            conn.execute('delete from samples')
            for i,x in enumerate(batch):
                conn.execute('insert into samples (sample, value) VALUES (%d, %f)' % (i,x))
            conn.commit()
            """
            """
            start = time.time()
            spectrum = fft(batch)
            amplitude = [(x.real**2 + x.imag**2)**(1/2) for x in spectrum]
            """
            """
            conn.execute('delete from spectrum')
            for i, (x,y) in enumerate(zip(amplitude, phase)):
                conn.execute('insert into spectrum (bucket, amplitude, phase) VALUES (%d, %f, %f)' % (i,x,y))
            conn.commit()
            """
            #np.savetxt('fft.csv', batch, delimiter=",")

except Exception as e:
    print(traceback.format_exc())
finally:
    os.close(fifo)
