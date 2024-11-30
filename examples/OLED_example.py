import machine
import ssd1306

i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("Hello, World!", 0, 0)
oled.show()
