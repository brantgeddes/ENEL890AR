import smbus, time, os
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
    print(e)

try:
    fifo = os.open(PIPE_NAME, os.O_WRONLY)
except Exception as e:
    print(e)
    exit()

try:
    next_read = time.time() + TIME_PERIOD
    i = 0
    msg = b''
    while True:
        if time.time() > next_read:
            next_read = time.time() + TIME_PERIOD
            conversion = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, 2)
            msg += conversion[0].to_bytes(1, byteorder='big')
            msg += conversion[1].to_bytes(1, byteorder='big')
            i += 1
            
            if i == N:
                os.write(fifo, msg)
                msg = b''
                i = 0

except Exception as e:
    print(e)
finally:
    os.close(fifo)

