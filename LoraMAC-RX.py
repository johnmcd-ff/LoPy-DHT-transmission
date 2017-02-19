from network import LoRa
import socket
import machine
import time
import pycom
import struct

def LoraDemoRun():
    #set to have no heart beat
    pycom.heartbeat(False)

    # initialize LoRa in LORA mode
    lora = LoRa(mode=LoRa.LORA, frequency=925000000)

    # create a raw LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    print("Started")
    while True:
        # send some data
        #s.setblocking(True)
        #s.send('Test1')
        #time.sleep(1)
        
        # wait to receive data
        time.sleep(1)
        data = s.recv(64)
        
        #if Data has been received
        if data != b'':
            #print(data)
            uData = struct.unpack("HhH",  data)
            print(hex (uData[0]), "\tTemperature:\t",  uData[1]/10, "C\tHumidity:\t\t",  uData[2]/10,  '%')
            #print ( '{}.{}'.format(uData[0]))
            pycom.rgbled(0x007f00) # green
            time.sleep(1)
            pycom.rgbled(0x000000) # off
            
LoraDemoRun()