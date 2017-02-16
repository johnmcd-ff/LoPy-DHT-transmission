from network import LoRa
import socket
import machine
import time
import pycom
import struct

rtc = machine.RTC()

# initialize LoRa in LORA mode
# more params can also be given, like frequency, tx power and spreading factor
print ("LoRa start")
lora = LoRa(mode=LoRa.LORA,  frequency=925000000,  tx_power=20)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

def sendtoLoRa(dev_ID,  temp,  hum):
    # send some data
    dev_time = rtc.now()

    datatosend = struct.pack('HhH', int(dev_ID, 16), temp,  hum)
    print('LoRa send: {}\n'.format(datatosend))
    s.setblocking(True)
    s.send(datatosend)
    #s.send(dev_ID, str([temp]),  str([hum]))
    s.setblocking(False)

    pycom.rgbled(0x001f00)  # LoRa heartbeat LED on
    time.sleep(2)			# pause 2s for next read
    pycom.rgbled(0x00001f)  # LoRa heartbeat LED off


