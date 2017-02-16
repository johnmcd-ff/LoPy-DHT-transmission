# LoPy-DHT-transmission
LoRa transmission of data from AM2302 temperature and humidity sensor

This project demonstrates sending of a temperature and humidity reading between a pair of Pycom LoPy devices.

The sensor is a DHT22 AM2302 device
http://wiki.seeed.cc/Grove-Temperature_and_Humidity_Sensor_Pro/
http://akizukidenshi.com/download/ds/aosong/AM2302.pdf

Wiring to the LoPy/expansion board is:

DHT22 pin   Signal    LoPy pin
  (1)       VDD       3V3
  (2)       SDA/data  P9/G16
  (3)       NC
  (4)       GND       GND
  
The code for this project is based on a onewire example for the DHT22 provided by"RinusW" on the MicroPython forum
https://forum.micropython.org/viewtopic.php?f=14&t=1392&sid=40eb4babb92000229de4a8eecc16b67b
This is an excellent write up and ought to be read in full.

The changes I had to do in order to make it work on the LoPy are:
1/  increase the sample size from 300 to 700, this ensures that the complete bit sequence is recieved.
2/  remove the first test for start bit, otherwise the sequence missed a bit and failed the CRC check.

The setup requires two LoPy, one to take readings from the sensor and transmit over LoRa; the second to receive the data and display.

The project files are:

main.py
  connects wifi locally, for convenience to display/debug on the local console
  update the realtime clock from an NTP server, not strictly required
  call the main loop to read data and transmit
  
homewifi.py
  connects to a local wifi access point.
  uses a separate file, wifi_name.txt, that contains the SSID and password for the wifi
  for convenience saves the device ID to a file, i.e. the last 4 digits of the MAC address of the device
  displays the IP settings on the console
  
ntp_time.py
  updates the real time clock with network time
  
DHT22RinusW-call.py
  initiates the DHT sensor
  runs a loop that reads the sensor and transmits the data on LoRa
  
DHT22RinusW.py
  starts the sensor data conversion
  samples the received data from the sensor, converts to bits, adds bits into a byte array, checks parity

LoraMAC.py
  initialises the LoRa module and creates a socket for transmission/reception
  sends the required data to the LoRa transmitter
  
  for reception, the simpler process of receiving the data and printing to the console.
