from message import decode_msg_size
import os, select, math, numpy as np

def get_message(fifo: int) -> str:
    msg_size_bytes = os.read(fifo, 4)
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size).decode("utf8")
    return msg_content

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

# Target sample rate
sample_rate = 490
# Batch size
N = 64
# Queue Named Pipe
PIPE_NAME='ADC_READ_PIPE'
os.mkfifo(PIPE_NAME)

try:
    fifo = os.open(PIPE_NAME, os.O_RDONLY)
except:
    print(e)
    exit()

try:
    while True:
        if fifo:
            batch = fifo.get_message(fifo)
            batch = dft(batch)
            print(batch)
except:
    print(e)
finally:
    os.close(fifo)
