import machine
import utime
from ds3231 import DS3231
import ssd1306

i2c_rtc = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
i2c_oled = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6))

rtc = DS3231(i2c_rtc)

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

# Set the time (year, month, day, weekday, hour, minute, second)
rtc.datetime((2024, 11, 29, 5, 19, 40, 0))

def read_rtc():
    try:
        current_time = rtc.datetime()
        year, month, day, weekday, hour, minute, second = current_time[:7]
        
        # Convert to US Central Time (UTC-6), Change your local Time
        hour = (hour - 6) % 24
        
        oled.fill(0)
        oled.text("Current Time:", 0, 0)
        oled.text(f"{year}-{month:02d}-{day:02d}", 0, 20)
        oled.text(f"{hour:02d}:{minute:02d}:{second:02d}", 0, 40)
        oled.show()
        
        print("Current Time:", current_time)
    except OSError as e:
        print("Failed to read RTC:", e)

# Main loop to read the RTC and update the OLED every 2 seconds
while True:
    read_rtc()
    utime.sleep(2)
