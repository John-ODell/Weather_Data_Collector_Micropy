import machine
i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6))
devices = i2c.scan()
if devices:
    print("I2C devices found:", devices)
else:
    print("No I2C devices found")
