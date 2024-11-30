import machine
import sdcard
import os
import time

spi = machine.SPI(0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))
cs = machine.Pin(5, machine.Pin.OUT)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

def write_test_file():
    try:
        with open("/sd/test_file.txt", "w") as file:
            file.write("Hello, SD card!")
        print("Test file written successfully.")
    except OSError as e:
        print(f"Error writing to SD card: {e}")

def read_test_file():
    try:
        with open("/sd/test_file.txt", "r") as file:
            content = file.read()
        print("Test file content:", content)
    except OSError as e:
        print(f"Error reading from SD card: {e}")

while True:
    write_test_file()
    time.sleep(2)
    read_test_file()
    time.sleep(2)
