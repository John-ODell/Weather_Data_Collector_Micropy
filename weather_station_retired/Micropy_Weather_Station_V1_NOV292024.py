import machine
import ssd1306
import dht
import onewire
import ds18x20
import sdcard
import os
import time

i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

dht11 = dht.DHT11(machine.Pin(28))

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
if not roms:
    raise Exception("No DS18B20 devices found!")
ds_rom = roms[0]

ldr = machine.ADC(machine.Pin(26))

spi = machine.SPI(0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))
cs = machine.Pin(5, machine.Pin.OUT)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

def log_data():
    try:
        dht11.measure()
        temp_dht_c = dht11.temperature()
        hum = dht11.humidity()
        ds_sensor.convert_temp()
        time.sleep(1)
        temp_ds_c = ds_sensor.read_temp(ds_rom)
        temp_dht_f = temp_dht_c * 9 / 5 + 32
        temp_ds_f = temp_ds_c * 9 / 5 + 32
        ldr_value = ldr.read_u16()

        with open("/sd/weather_data.csv", "a") as file:
            file.write(f"{time.localtime()},{temp_dht_c},{temp_dht_f},{hum},{temp_ds_c},{temp_ds_f},{ldr_value}\n")
    except OSError as e:
        print(f"Error logging data: {e}")

def display_data():
    try:
        dht11.measure()
        temp_dht_c = dht11.temperature()
        hum = dht11.humidity()
        ds_sensor.convert_temp()
        time.sleep(1)
        temp_ds_c = ds_sensor.read_temp(ds_rom)
        temp_dht_f = temp_dht_c * 9 / 5 + 32
        temp_ds_f = temp_ds_c * 9 / 5 + 32
        ldr_value = ldr.read_u16()

        oled.fill(0)
        oled.text("Weather Station", 0, 0)
        oled.text(f"DHT Temp: {temp_dht_f}F", 0, 20)
        oled.text(f"Humidity: {hum}%", 0, 30)
        oled.text(f"DSB Temp: {temp_ds_f}F", 0, 40)
        oled.text(f"LDR: {ldr_value}", 0, 50)
        oled.show()
    except OSError as e:
        print(f"Error displaying data: {e}")

log_interval = 1800  # 30 minutes in seconds
last_log_time = time.time()

while True:
    display_data()
    current_time = time.time()
    if current_time - last_log_time >= log_interval:
        log_data()
        last_log_time = current_time
    time.sleep(2)  # Update display every 2 seconds
