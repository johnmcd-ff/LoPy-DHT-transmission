import time
import pycom
from machine import Pin
from LoraMAC import sendtoLoRa
from DHT22RinusW import DHT22
from DHT22RinusW import DHT11

def go_DHT():
    dht_pin=Pin('P9', Pin.OPEN_DRAIN)	# connect DHT22 sensor data line to pin P9/G16 on the expansion board
    dht_pin(1)							# drive pin high to initiate data conversion on DHT sensor
    
    while (True):
        temp, hum = DHT11(dht_pin)
        # temp = temp * 9 // 5 + 320   # uncomment for Fahrenheit
        temp_str = '{}.{}'.format(temp//10,temp%10)
        hum_str = '{}.{}'.format(hum//10,hum%10)
        # Print or upload it
        print('temp = {}C; hum = {}%'.format(temp_str, hum_str))
        if hum!=0xffff:
            sendtoLoRa(dev_ID,  temp,  hum)
        time.sleep(2)
 
pycom.heartbeat(False)
pycom.rgbled(0x1f0000)    # turn LED blue


f=open('device_name.py')   #get device name from file
dev_ID = f.read()
print(dev_ID)

go_DHT()

