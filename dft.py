from message import decode_msg_size
import os, select, math, traceback, numpy as np

# Target sample rate
sample_rate = 490
# Batch size
N = 64
# Queue Named Pipe
PIPE_NAME='ADC_READ_PIPE'

def get_message(fifo: int) -> str:
    frame = os.read(fifo, 2 * N)
    msg = [ x for x in frame ]#[ int.from_bytes(x, byteorder='little') for x in msg ]
    data = np.array([])
    print(len(msg))
    for i in range(0, N * 2, 2):
        data = np.append(data, msg[i] + msg[i + 1] * 16**2)
    print(len(data))
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
    while True:
        if fifo:
            batch = get_message(fifo)
            batch = dft(batch)
            np.savetxt('dft.csv', batch, delimiter=",")
except Exception as e:
    print(traceback.format_exc())
finally:
    os.close(fifo)
