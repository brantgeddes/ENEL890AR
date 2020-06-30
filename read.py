import smbus, time, os, traceback
from message import create_msg

bus = smbus.SMBus(1)

DEVICE_ADDRESS = 0x48
TIME_PERIOD = 1/490
N = 64
PIPE_NAME='ADC_READ_PIPE'


try:
    config = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x01, 2)
    if config[0] == 68 and config[1] == 67:
        print("Config register set")
    else:
        print("Setting Config register")
        bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x44, 0x43]) 
except Exception as e:
    print(traceback.format_exc())

try:
    fifo = os.open(PIPE_NAME, os.O_WRONLY)
except Exception as e:
    print(traceback.format_exc())
    exit()

try:
    next_read = time.time() + TIME_PERIOD
    while True:
        if time.time() > next_read:
            next_read = time.time() + TIME_PERIOD
            conversion = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, 2)
            conversion = (conversion[0]<<4) | (conversion[1]>>4)
            print(conversion)
            msg = conversion.to_bytes(2, byteorder='big')
            os.write(fifo, msg)

except Exception as e:
    print(traceback.format_exc())
finally:
    os.close(fifo)

