import machine
import ssd1306
import dht
import time
from ds3231 import DS3231

i2c_oled = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6))
i2c_rtc = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

dht_sensor = dht.DHT11(machine.Pin(15))

uv_sensor = machine.ADC(machine.Pin(26))

rtc = DS3231(i2c_rtc)

# Set the time (year, month, day, weekday, hour, minute, second)
rtc.datetime((2024, 11, 29, 5, 19, 40, 0))

def display_data():
    try:
        dht_sensor.measure()
        temp_c = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        temp_f = temp_c * 9 / 5 + 32

        uv_value = uv_sensor.read_u16()
        uv_voltage = uv_value / 1024 * 5.0

        current_time = rtc.datetime()
        year, month, day, weekday, hour, minute, second = current_time[:7]

        hour = (hour - 6) % 24

        oled.fill(0)
        oled.text("Weather Station", 0, 0)
        oled.text(f"Date: {year}-{month:02d}-{day:02d}", 0, 10)
        oled.text(f"Time: {hour:02d}:{minute:02d}:{second:02d}", 0, 20)
        oled.text(f"Temp: {temp_f:.1f}F", 0, 30)
        oled.text(f"Humidity: {hum}%", 0, 40)
        oled.text(f"UV: {uv_voltage:.2f}V", 0, 50)
        oled.show()

        print("Current Time:", current_time)
        print(f"Temp: {temp_f:.1f}F, Humidity: {hum}%, UV: {uv_voltage:.2f}V")
    except OSError as e:
        print(f"Error displaying data: {e}")

# Main loop to read sensors and update the OLED every 2 seconds
while True:
    display_data()
    time.sleep(2)
