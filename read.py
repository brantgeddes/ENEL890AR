import smbus, time, os
from message import create_msg

bus = smbus.SMBus(1)

DEVICE_ADDRESS = 0x48
TIME_PERIOD = 1/490

PIPE_NAME='ADC_READ_PIPE'


try:
    config = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x01, 2)
    if config[0] == 68 and config[1] == 67:
        print("Config register set")
    else:
        print("Setting Config register")
        bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x44, 0x43]) 
except:
    print(e)
    exit()

try:
    fifo = os.open(PIPE_NAME, os.O_WRONLY)
except:
    print(e)
    exit()

try:
    next_read = time.time() + TIME_PERIOD
    while True:
        if time.time() > next_read:
            next_read = time.time() + TIME_PERIOD
            conversion = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, 2)
            conversion = conversion[0] * 16**2 + conversion[1]
            os.write(fifo, conversion)
except:
    print(e)
finally:
    os.close(fifo)

