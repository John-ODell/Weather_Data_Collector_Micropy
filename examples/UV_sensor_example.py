import machine
import time

uv_sensor = machine.ADC(machine.Pin(26))

def read_uv():
    try:
        uv_value = uv_sensor.read_u16()
        # UV light value equation: V = sensorValue / 1024 * 5.0
        # Set for 5v, can change for 3.3v though a constant can still be analyzed 
        uv_voltage = uv_value / 1024 * 5.0
        print("UV Sensor Value: {}, UV Voltage: {} V".format(uv_value, uv_voltage))
    except OSError as e:
        print("Failed to read UV sensor:", e)

while True:
    read_uv()
    time.sleep(2)

"""
Let’s dive into the code to understand how it works:

The code starts by initializing the serial communication in the void setup.
In the void loop, the code starts by declaring a variable for the sensor reading.
The code then reads the value from the analog input 0 and converts it to a voltage using the formula V=sensorValue/1024*5.0.
The following line of code prints out “sensor reading =” followed by whatever was read from A0.
Then it prints out “sensor voltage =” followed by what was calculated earlier.
Finally, it prints out “V” to represent the voltage.
The sensorValue variable stores the result of the conversion, which is then printed out on the Serial Monitor.
"""
