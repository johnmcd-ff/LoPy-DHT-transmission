import machine
import pycom
import time
import binascii
from network import WLAN


pycom.heartbeat(False)      # turn off the heartbeat LED so that it can be reused

deviceID=binascii.hexlify(machine.unique_id())   # get device unique id and save to file on device
print (deviceID[8:12])

f_wifi = open('/flash/homewifi/wifi_name.txt', 'r')     # read wifi SSID and password from file, keeps secret data separate from the code
                                                        # file format is:  SSID, WLAN.WPA2, password
wifi_setting = f_wifi.readline()
wifi_strings = [i.strip() for i in wifi_setting.split(',')]
f_wifi.close()

print(wifi_strings[0],  wifi_strings[1],  wifi_strings[2])

f=open('/flash/device_name', 'w''')				# write the deviceID to a file for reference
f.write(deviceID[8:12])
f.close()

print('led on')
pycom.rgbled(0x7f0000)		# red
time.sleep(2)

wlan = WLAN(mode=WLAN.STA)
wlan.connect(wifi_strings[0],  auth=(wifi_strings[1], wifi_strings[2]), timeout = 5000)
print('wifi connecting')
while not wlan.isconnected():
	machine.idle()  #loop until connected

pycom.rgbled(0x00007f)		# blue

time.sleep(1)
pycom.rgbled(0x007f00)		# green

print(wlan.ifconfig())		# print the allocated IP settings
