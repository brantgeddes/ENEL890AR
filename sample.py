import logging, traceback, time, smbus
from cmath import exp, pi
import random
import timeit

bus = smbus.SMBus(1)

class Sample:
    N = 32
    PERIOD = 1/920
    DEVICE_ADDRESS = 0x48
    sin_values = [ 0, 0.5235, 0.7854, 1.0174, 1.5708, 3.1416, 1.5708, 1.0174, 0.7854, 0.5235, 0, -0.5235, -0.7854, -1.0174, -1.5708, -3.1416, -1.5708, -1.0174, -0.7854, -0.5235 ]
    def __init__(self):
        try:
            self.batch = [0] * self.N
            config = bus.read_i2c_block_data(self.DEVICE_ADDRESS, 0x01, 2)
            if config[0] == 68 and config[1] == 67:
                print(config)
                print("Config register set")
            else:
                print("Setting Config register")
                bus.write_i2c_block_data(self.DEVICE_ADDRESS, 0x01, [0x44, 0x43]) 
        except Exception as e:
            logging.exception(traceback.format_exc())

    def run(self, pipeline):
        try:
            current_time = time.time()
            while not pipeline.should_exit():
                if time.time() > current_time + self.PERIOD:
                    current_time = time.time()
                    self.pipeline = pipeline
                    conversion = bus.read_i2c_block_data(self.DEVICE_ADDRESS, 0x00, 2)
                    conversion = (conversion[0]<<4) | (conversion[1]>>4)
                    self.batch.append(conversion)
                    self.batch.pop(0)
                    spectrum = self.fft(self.batch)
                    print(self.batch)
                    pipeline.emit(self.batch, spectrum)
        except Exception as e:
            logging.exception(traceback.format_exc())

    def fft(self, batch):
        N = len(batch)
        if N <= 1: return batch
        even_side = self.fft(batch[0::2])
        odd_side = self.fft(batch[1::2])
        T = [exp(-2j*pi*k/N)*odd_side[k] for k in range(N//2)]
        return [even_side[k] + T[k] for k in range(N//2)] + [even_side[k] - T[k] for k in range(N//2)]
