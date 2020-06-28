import smbus, time

bus = smbus.SMBus(1)

DEVICE_ADDRESS = 0x48
TIME_PERIOD = 1/490

#bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x44, 0x43])

#print(bus.read_block_data(DEVICE_ADDRESS, 0x00))

try:
    config = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x01, 2)
    if config[0] == 68 and config[1] == 67:
        print("Config register set")
    else:
        print("Setting Config register")
        bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x44, 0x43]) 
except:
    print(e)

next_read = time.time() + TIME_PERIOD
while True:
    if time.time() > next_read:
        next_read = time.time() + TIME_PERIOD
        conversion = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, 2)
        print(conversion[0] + conversion[1])
