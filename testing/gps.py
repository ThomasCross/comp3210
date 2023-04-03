import time
import serial
import json

import adafruit_gps

uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

#last_print = time.monotonic()
while True:

    gps.update()

    #current = time.monotonic()
    #if current - last_print >= 1.0:
        #last_print = current

    time.sleep(1)
    if not gps.has_fix:
        print('Waiting for fix...')
        continue
    #print('=' * 40)  # Print a separator line.
    #print('Latitude: {0:.6f} degrees'.format(gps.latitude))
    #print('Longitude: {0:.6f} degrees'.format(gps.longitude))

    coords = {
        "lat": float("{0:.6f}".format(gps.latitude)),
        "long": float("{0:.6f}".format(gps.longitude))
    }

    print(json.dumps(coords))