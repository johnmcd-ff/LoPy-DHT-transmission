from machine import enable_irq, disable_irq
import time

# this onewire protocol code tested with Pycom LoPy device and AM2302/DHT22 sensor

def getval(pin):
    ms = [1]*700        # needs long sample size to grab all the bits from the DHT
    time.sleep(1)
    pin(0)
    time.sleep_us(10000)
    pin(1)
    irqf = disable_irq()
    for i in range(len(ms)):
        ms[i] = pin()      ## sample input and store value
    enable_irq(irqf)
    #for i in range(len(ms)):		#print debug for checking raw data
    #   print (ms[i])
    return ms

def decode(inp):
    res= [0]*5
    bits=[]
    ix = 0
    try:
        #if inp[0] == 1 : ix = inp.index(0, ix) ## skip to first 0	# ignore first '1' as probably sample of start signal.  *But* code seems to be missing the start signal, so jump this line to ensure response signal is identified in next two lines.
        ix = inp.index(1,ix) ## skip first 0's to next 1	#  ignore first '10' bits as probably the response signal.
        ix = inp.index(0,ix) ## skip first 1's to next 0
        while len(bits) < len(res)*8 : ##need 5 * 8 bits :
            ix = inp.index(1,ix) ## index of next 1
            ie = inp.index(0,ix) ## nr of 1's = ie-ix
								# print ('ie-ix:',ie-ix)
            bits.append(ie-ix)
            ix = ie
    except:
        print('6: decode error')
        # print('length:')
        # print(len(inp), len(bits))
        return([0xff,0xff,0xff,0xff])

    # print('bits:', bits)
    for i in range(len(res)):
        for v in bits[i*8:(i+1)*8]:   #process next 8 bit
            res[i] = res[i]<<1  ##shift byte one place to left
            if v >= 7:                   #  less than 7 '1's is a zero, 7 or more 1's in the sequence is a one
                res[i] = res[i]+1  ##and add 1 if lsb is 1
            # print ('res',  i,  res[i])

    if (res[0]+res[1]+res[2]+res[3])&0xff != res[4] :   ##parity error!
        print("Checksum Error")
        print (res[0:4])
        res= [0xff,0xff,0xff,0xff]

    # print ('res:', res[0:4])
    return(res[0:4])

def DHT11(pin):
    res = decode(getval(pin))
    temp = 10*res[0] + res[1]
    hum = 10 * res[2] + res[3]
    return temp, hum
   
def DHT22(pin):
    res = decode(getval(pin))
    hum = res[0]*256+res[1]
    temp = res[2]*256 + res[3]
    if (temp > 0x7fff):
        temp = 0x8000 - temp
    return temp, hum   
