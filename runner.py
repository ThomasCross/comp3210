from comp3210.helpers.gps import GPS
from comp3210.helpers.lcd import LCD
from comp3210.helpers.xbee import Xbee, XBeeAddress
import time
import json

gps = GPS()
lcd = LCD()
xbee = Xbee()

LOOP = 5

counter = LOOP
while True:
    time.sleep(1)
    if counter > 0:
        counter -= 1

        lcd.lcd_display_string("Count to signal:              ", 1, 0)
        lcd.lcd_display_string("{} Seconds                   ".format(counter), 2, 0)

    else:
        counter = LOOP

        wait = 0
        while True:
            lat, long = gps.get_lat_long()
            print("{}, {}".format(lat, long))

            coords = {
                "lat": float(lat),
                "long": float(long)
            }

            if lat != None:
                break
            else:
                wait += 1
                lcd.lcd_display_string("Wait GPS connect             ", 1, 0)
                lcd.lcd_display_string("{}                           ".format(wait), 2, 0)
                time.sleep(1)

        lcd.lcd_display_string("Sending signal!              ", 1, 0)
        lcd.lcd_display_string("                             ", 2, 0)

        # dispatch to xbee
        xbee.send(json.dumps(coords), XBeeAddress.P)

        
    
    