from message import decode_msg_size
import os, select, math, traceback, numpy as np
import sqlite3

# Target sample rate
sample_rate = 490
# Batch size
N = 64
# Queue Named Pipe
PIPE_NAME='ADC_READ_PIPE'

conn = sqlite3.connect('data.db')

def get_message(fifo: int) -> str:
    frame = os.read(fifo, 2 * N)
    msg = [ x for x in frame ]#[ int.from_bytes(x, byteorder='little') for x in msg ]
    msg = [(3.3 * x / 4095) for x in msg ]
    data = np.array([])
    for i in range(0, len(msg), 2):
        data = np.append(data, msg[i + 1] + msg[i] * 16**2)
    return data

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
    batch = np.array([])
    i = 0
    while True:
        if fifo:
            new_batch = get_message(fifo)
            i += len(new_batch)
            batch = np.append(batch, new_batch)
            if i >= N:
                batch = batch[0:64]
                conn.execute('delete from samples')
                for i,x in enumerate(batch):
                    conn.execute('insert into samples (sample, value) VALUES (%d, %f)' % (i,x))
                conn.commit()
                real, imag = dft(batch)
                conn.execute('delete from dft')
                for i, (x,y) in enumerate(zip(real, imag)):
                    conn.execute('insert into dft (bucket, real, imag) VALUES (%d, %f, %f)' % (i,x,y))
                conn.commit()
                batch = []
                i = 0
except Exception as e:
    print(traceback.format_exc())
finally:
    os.close(fifo)
