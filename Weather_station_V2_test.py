import machine
import ssd1306
import dht
import sdcard
import os
import time
from ds3231 import DS3231

i2c_oled = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6))
i2c_rtc = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

dht_sensor1 = dht.DHT11(machine.Pin(15))
dht_sensor2 = dht.DHT11(machine.Pin(14))

uv_sensor = machine.ADC(machine.Pin(26))

spi = machine.SPI(0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))
cs = machine.Pin(5, machine.Pin.OUT)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

rtc = DS3231(i2c_rtc)

# Set the time (year, month, day, weekday, hour, minute, second)
rtc.datetime((2024, 11, 29, 5, 20, 47, 0))

def log_data():
    try:
        dht_sensor1.measure()
        temp_c1 = dht_sensor1.temperature()
        hum1 = dht_sensor1.humidity()
        temp_f1 = temp_c1 * 9 / 5 + 32

        dht_sensor2.measure()
        temp_c2 = dht_sensor2.temperature()
        hum2 = dht_sensor2.humidity()
        temp_f2 = temp_c2 * 9 / 5 + 32

        uv_value = uv_sensor.read_u16()
        uv_voltage = uv_value / 1024 * 5.0

        current_time = rtc.datetime()
        year, month, day, weekday, hour, minute, second = current_time[:7]

        with open("/sd/weather_data.csv", "a") as file:
            file.write(f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d},{temp_c1},{hum1},{temp_c2},{hum2},{uv_value},{uv_voltage}\n")
    except OSError as e:
        print(f"Error logging data: {e}")

def display_data():
    try:
        dht_sensor1.measure()
        temp_c1 = dht_sensor1.temperature()
        hum1 = dht_sensor1.humidity()
        temp_f1 = temp_c1 * 9 / 5 + 32

        dht_sensor2.measure()
        temp_c2 = dht_sensor2.temperature()
        hum2 = dht_sensor2.humidity()
        temp_f2 = temp_c2 * 9 / 5 + 32

        uv_value = uv_sensor.read_u16()
        uv_voltage = uv_value / 1024 * 5.0

        current_time = rtc.datetime()
        year, month, day, weekday, hour, minute, second = current_time[:7]

        # Convert to US Central Time (UTC-6)
        hour = (hour - 6) % 24
        am_pm = "AM" if hour < 12 else "PM"
        hour_display = hour % 12
        if hour_display == 0:
            hour_display = 12

        oled.fill(0)
        oled.text("Weather Station", 0, 0)
        oled.text(f"Date: {year}-{month:02d}-{day:02d}", 0, 10)
        oled.text(f"Time: {hour_display:02d}:{minute:02d}:{second:02d} {am_pm}", 0, 20)
        oled.text(f"TEMP1: {temp_f1:.1f}F ({hum1}%)", 0, 30)
        oled.text(f"TEMP2: {temp_f2:.1f}F ({hum2}%)", 0, 40)
        oled.text(f"UV: {uv_voltage:.2f}V", 0, 50)
        oled.show()

        print("Current Time:", current_time)
        print(f"TEMP1: {temp_f1:.1f}F ({hum1}%), TEMP2: {temp_f2:.1f}F ({hum2}%), UV: {uv_voltage:.2f}V")
    except OSError as e:
        print(f"Error displaying data: {e}")

# Main loop to read sensors, update the OLED, and log data every 2 seconds
while True:
    display_data()
    log_data()
    time.sleep(2)
