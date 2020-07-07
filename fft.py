import collections, logging, traceback, time
from cmath import exp, pi

class FFT:
    def __init__(self):
        try:
            pass
        except Exception as e:
            logging.exception(traceback.format_exc())

    def run(self, pipeline):
        try:
            batch = collections.deque(maxlen=16)
            start = time.time()
            while not pipeline.should_exit():
                print(pipeline.signal, pipeline.spectrum)
                #batch.append(pipeline.consume())
                #batch = pipeline.consume()
                #print(batch)
                #fft = self.fft(batch)
                #amplitude = [ (x.real**2 + x.imag**2)**(1.2) for x in fft ]
                #print(amplitude)
        except Exception as e:
            logging.exception(traceback.format_exc())

    def fft(self, x):
        N = len(x)
        if N <= 1: return x
        even = self.fft(x[0::2])
        odd = self.fft(x[1::2])
        T = [exp(-2j*pi*k/N)*odd[k] for k in range(N//2)]
        return [even[k] + T[k] for k in range(N//2)] + [even[k] - T[k] for k in range(N//2)]