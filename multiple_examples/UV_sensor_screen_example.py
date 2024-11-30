import machine
import ssd1306
import time

i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

uv_sensor = machine.ADC(machine.Pin(26))

def display_data():
    try:
        uv_value = uv_sensor.read_u16()

        oled.fill(0)
        oled.text("Weather Station", 0, 0)
        oled.text(f"UV: {uv_value}", 0, 20)
        oled.show()
    except OSError as e:
        print(f"Error displaying data: {e}")

while True:
    display_data()
    time.sleep(2)  # Update display every 2 seconds
