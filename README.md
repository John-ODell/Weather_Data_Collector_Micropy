Weather Station Data Collection in Micro Python by John O'Dell

We have used Circuit Python in past examples to use an SD card with our Pi Pico's. I am happy to say I have gotten SD cards to to work with them in Micro Python, something I have had trouble with getting stable in the past. I have only got it to work with a 1gb card, that will be enough for this test.

This is an issue with the baudrate, partitions, and timing. I am still learning and will update when I have a stable version for cards 16gb and larger. 

This Sketch Will be used In the month of December 2024 for its first data collection.

ITEMS NEEDED

    - Pi Pico (Tested on Pi Pico 2)
    - DHT 11 (two are wired in the sketch, DHT11 fail rate is high)
    - UV light sensor
    - DS3231 RTC
        - CR3202 Battery
    - Micro SD Card Reader
        - 1gb SD card !!!!!!!!!!!!!!! MUST BE 1GB !!!!!!!
        - THIS IS STABLE FOR MICRO PYTHON NOW, I AM WORKING ON LARGER PARTITIONS
    - .96 OLED Screen
    - Breadboard
    - Jumperwire
    - Thonny IDE https://thonny.org/

**** Flashing MicroPython *****
Jump To the Bottom if your need to set up your Pi Pico for the first time or it is not being reconized by Thonny. Otherwise use Thonny to flash the most recent version of MicroPython to your device.

Packages Required

Navigte to Tools in the top left corner
   
    - Manage Packages
    - Type in these name and install, you will see a list gather on the left hand side
        - 12cdevice
        - onewire
        - sdcard
        - smbus2

Open the requirments folder from the github download
Save both sketches to the devices named respectively

    - File
        - Save As
            - To this device
                - "ds3231.py"
                - "ssd1306.py"

--You will need to have both the packages and reference sketches before running any of the following code.----
    

DHT 11 (2 wired in sketch in case of a failure)
Pin Outs

    - VCC -> 3.3v
    - GND -> GND
    - S -> GPIO 14 (DHT#1)
    - S -> GPIO 15 (DHT#2)

Open the sketch "DHT11_example.py"

    - Press the green arrow (Run)
    - On the serial monitor you will see the temperature and humitidy returned.
    - Change the Pin Number to your DHT11#2 to ensure both are working or if you are using another pin

UV Light Sensor
Pin Outs

    - VCC -> 3.3v
    - GND -> GND
    - S -> GPIO 22

Open the sketch "UV_sensor_example.py"

    - Press the green arrow (Run)
    - On the serial Moniter you see th UV value return in a V value
    - Please read the description in the sketch for an explination on how the V value is calculated. The sketch does follow the descriptions equation for V value, though I believe it is set for  5v VCC. Feel free to change the Equation for a different way to read the V value.

DS3231 RTC (Real Time Clock)
Pin Outs

    - VCC -> 3.3v
    - GND -> GND
    - S -> GPIO 26

Open the sketch "RTC_test_example"

    - Replace the time if wanted withing the rtc.datetime((year,month,day,weekday,24hour,minute,second))
    - Press the green arrows (Run)
    - In the serial monitor you will see the time start to return in the same format
        - the seconds will return updating, leave the example runnning for as long as you would like to test the unit. 

Micro SD Card 
Pin Outs

    - VCC -> 3.3v
    - GND -> GND
    - SCK -> GPIO 2
    - MOSI -> GPIO 3
    - MISO -> GPIO 4
    - CS -> GPIO 5

Open the sketch "sd_test_example.py"
Make sure you are in 3.3v, it is fine to pull from the main rail breadbaord to the Micro SD Reader.

    - A test file will be written to the sd card
    - In the serial monitor this a message that the file has been written will be repeated
    - You may not be able to view to newly saved file from thonny, thats to be expected
        - Remove the Micro Sd card from the module and read it into a computer
        - Make sure the test file has been written
        - Feel free to delete the file on the micro sd card once the test has worked

.96 OLED Display
Pin Outs

    - VCC -> 3.3v
    - GND -> GND
    - SCL/SCK -> GPIO 7
    - SDA -> GPIO 6

"Hello World" will display at the top of the screen. 

    - Change the 0,0 (x,y) coordinates for placement
    - Change withing the  "" for a different text
    - use the command oled.text("New Line",0,10) to add another line of text to the screen

Multiple Examples Together

After you get all the examples running, I found it best to run a few more to make sure there are no communication errors. This can happen when using multiple i2c ports. If you get and error, first return to the examples and make it sure it works before running these.

----EO/EOI TIME OUT ERROR-----
If you get this error, one or more of the i2c ports are not communicating or interfacing in the sketch.

    - Open "i2c_scan.py"
    - replace the scl/sda pins with yours
    - look at the Raspberry Pi Pico pinout reference diagram
    - SDA/SCL will be on i2c 0 or 1
        - Pin 6 and 7 are on i2c 1
        - Pin 8 and 9 are on 12c 0
    - Press Run (green arrow) Find the address (0x#)
    - If no address is found, there is a communication error to with the module.
    - If an address is found, there is a communication error with the sketch.
    - If this probelm persist try changing all i2c ports, or un plugging the Pi Pico
    - A bad DHT11 not communicating with screen can lead to this error
    - You must have all requirments and references sketches on the Pi Pico device

Open the sketch "RTC_test_example"

    - Press the green arrow (Run)
    - The time will be displayed to the top of the screen
    - Change the time using a 24hour format to the desired time and coordinates for placement
    - refer to the eoi timeout if it does not display
        - 12 hour time may or may not work correctly past noon. I recommend 24 hour for saving the time aswell
    
Open the sketch  "UV_sensor_screen_example"

    - Press the green arrow (Run)
    - The UV will return in V to the OLED screen
    - Refer to the EOI above for a timeout
    - for other errors check the UV sensor module

Open the sketch "Weather_Station_OLED

    - Press the green arrow (Run)
    - The Sensors will read the OLED screen
        - The Date, Time, Both DHT11, and the UV in V
    - Adjust the oled.print how you would like

--WEATHER STATION--

Before running the main sketch

    - Save the Required sketches to the Pi Pico
    - Install the Required Packages from the Package Manager in Thonny
    - Run the example sketches to test the modules
    - you have a battery in the DS3231 Real Time Clock Module
    - You have TWO DHT11's or comment out one from the sketch
    - You have flashed the most recent version of MicroPython to your Pi Pico

Weather_station_V1 (obsolete) 
 
    - timestamp did not save correctly
        - timestamp and date are now seperated in two different columns
    - 12 hour time did not want to work all the time
        - changed to 24 hour in save and screen
    - Removed Digital Thermometor and added second DHT11 for better accuracy

Weather_station_v2_test (Micro SD Card Test)
    
    - Test the SD card saving data in a CSV format, taking a sample every 2 seconds
    - This fast of a sample can mess with the timestamp, estend the sample rate and format to ensure a time stamp is stable

Weather_Station_V2_Boot 

    - Press the green arrow to run the example
        - Save sketch to the Pi Pico and rename as "boot.py" to have run when it is powered by usb
            - Thonny will not reconize the device once this has happned.
            - To stop a boot.py follow the FLASH MICROPYTHON instructions

    - This will take a sample from all of the sensors every 20 seconds, save it in a csv format, and display them in real time along with the date and time on the OLED screen.
    - (Time, Date, DHT#1 C, DHT#1 F, DHT#1 H%, DHT#2 C, DHT#2 F, DHT#2 H%, UV raw, UV in V)
    - It updates the screen with all the data including the date and real time every 15 seconds. This is to help draw less power than updating in real time. Feel free to change this based on your consumption needs.
    
This project is designed to collect data for 31 days before removing the sd card for analysis. There was a 24 hour test to esnure the accuracy of and ability to record data.

It is recommended to do this is in a covered area or where the materials will not be exposed to rain. Maintain the equipment daily for the best results. 

**** Flashing Micro Python *****

Open Thonny and Navigate to the Top Right

    - Click Run
    - Click Configure Interpreter 
        - Bottom left
        - Install or Update MicroPython
    - Target Volume
        - Auto Detected 
            -If not, RP1/RP2 or the name of the device
    - Micro Python Family
        - RP2
    - Variant
        - Pi Pico/W/2 Depending on your Model
    - Version
        - Most Recent
    - Install

Once Installed Close both windows and Click Run in the Top right

    - Click Configure Interpreter
        - Which Kind of Interpreter Should Thonny Use
            - MicroPython (Raspberry Pi Pico)
        - Port or WebREPL 
            - Auto Detected Or a COMS# Port
                - Click on the Dropdown to see
    - Press Ok
    -Click the Red stop Botton and in the serial monitor you will see your board

Reflashing **
If something goes wrong, you are suck in a boot, or your device is not being reconized

    - Unplug the Pi Pico
    - Hold the BOOT button on the Pi Pico and Plug the USB into your computer
    - Open the RP1/RP2 folder in your files
    - drag over the "flash_nuke.uf2"
        - use the 2040 for a pi pico 1 and W
        - use the 2350 for a pi pico 2
    - Start the flashing instructions again