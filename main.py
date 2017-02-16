# main.py -- put your code here!
# main.py for DHT sensor
# setup wifi
# start DHT loop


import time

print('start DHT loop')
execfile('/flash/homewifi/homewifi.py')		# connect to wifi
time.sleep(5)
execfile('/flash/homewifi/ntp_time.py')		# correct the RTC time to GMT
execfile('/flash/DHT22RinusW-call.py')      # start DHT loop
    

