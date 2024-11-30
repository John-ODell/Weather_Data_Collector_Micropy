import utime
import machine
from micropython import const

DATETIME_REG = const(0)
SECONDS_REG = const(0)
MINUTES_REG = const(1)
HOURS_REG = const(2)
WEEKDAY_REG = const(3)
DAY_REG = const(4)
MONTH_REG = const(5)
YEAR_REG = const(6)
CONTROL_REG = const(14)
STATUS_REG = const(15)

def dectobcd(decimal):
    return (decimal // 10) << 4 | (decimal % 10)

def bcdtodec(bcd):
    return ((bcd >> 4) * 10) + (bcd & 0x0F)

class DS3231:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self._timebuf = bytearray(7)
        self._buf = bytearray(1)

    def datetime(self, dt=None):
        if dt is None:
            self.i2c.readfrom_mem_into(self.addr, DATETIME_REG, self._timebuf)
            seconds = bcdtodec(self._timebuf[0])
            minutes = bcdtodec(self._timebuf[1])
            hour = bcdtodec(self._timebuf[2] & 0x3F)
            weekday = bcdtodec(self._timebuf[3])
            day = bcdtodec(self._timebuf[4])
            month = bcdtodec(self._timebuf[5] & 0x1F)
            year = bcdtodec(self._timebuf[6]) + 2000
            return (year, month, day, weekday, hour, minutes, seconds)
        else:
            self._timebuf[0] = dectobcd(dt[6])
            self._timebuf[1] = dectobcd(dt[5])
            self._timebuf[2] = dectobcd(dt[4])
            self._timebuf[3] = dectobcd(dt[3])
            self._timebuf[4] = dectobcd(dt[2])
            self._timebuf[5] = dectobcd(dt[1])
            self._timebuf[6] = dectobcd(dt[0] - 2000)
            self.i2c.writeto_mem(self.addr, DATETIME_REG, self._timebuf)

    def OSF(self):
        return bool(self.i2c.readfrom_mem(self.addr, STATUS_REG, 1)[0] >> 7)

    def _OSF_reset(self):
        self.i2c.readfrom_mem_into(self.addr, STATUS_REG, self._buf)
        self.i2c.writeto_mem(self.addr, STATUS_REG, bytearray([self._buf[0] & 0x7F]))


i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

rtc = DS3231(i2c)
# Set the time (year, month, day, weekday, hour, minute, second)
rtc.datetime((2024, 11, 29, 5, 19, 40, 0))

def read_rtc():
    try:
        current_time = rtc.datetime()
        print("Current Time:", current_time)
    except OSError as e:
        print("Failed to read RTC:", e)

# Main loop to read the RTC every 2 seconds, use .1 for miliseconds 
while True:
    read_rtc()
    utime.sleep(2)
