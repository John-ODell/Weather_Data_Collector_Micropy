import machine
import time
import dht

dht_sensor = dht.DHT11(machine.Pin(15))

def read_dht11():
    try:
        dht_sensor.measure()
        temperature_c = dht_sensor.temperature()  # Temperature in Celsius
        humidity = dht_sensor.humidity()          # Humidity in percentage
        temperature_f = temperature_c * 9 / 5 + 32  # Convert to Fahrenheit
        print("Temperature: {}°C / {}°F, Humidity: {}%".format(temperature_c, temperature_f, humidity))
    except OSError as e:
        print("Failed to read sensor:", e)

# Main loop to read the sensor every 2 seconds
while True:
    read_dht11()
    time.sleep(2)
