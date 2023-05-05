from comp3210.helpers.gps import GPS
from comp3210.helpers.lcd import LCD
from comp3210.helpers.xbee import Xbee, XbeeListener, XBeeAddress
import time
import json

gps = GPS()
lcd = LCD()
xbee = Xbee()

# Stops range being shown if seeker indicates less than 50m
in_range = False
def in_range_alert(address, message):
    global in_range
    if message == '0':
        in_range = False
    else:
        in_range = True

# Adds in_range_alert function to listener pool
listener = XbeeListener(in_range_alert)
xbee.add_listener(listener)

# Main loop
LOOP = 5
counter = LOOP
while True:
    time.sleep(1)
    # Count to signal time
    if counter > 0:
        counter -= 1

        lcd.lcd_display_string("Next (sec): {}    ".format(counter), 1, 0)

        if in_range:
            lcd.lcd_display_string("Seeker Nearby              ", 2, 0)
        else:
            lcd.lcd_display_string("Safe                       ", 2, 0)

    # Send signal
    else:
        counter = LOOP

        wait = 0
        while True:
            lat, long = gps.get_gps()
            print("{}, {}".format(lat, long))

            if lat == None:
                wait += 1

                lcd.lcd_display_string("Wait GPS connect             ", 1, 0)
                lcd.lcd_display_string("{} sec                       ".format(wait), 2, 0)
                time.sleep(1)

                continue

            coords = [float(lat), float(long)]
            
            break
                
        
        # Send signal
        lcd.lcd_display_string("Sending signal!              ", 1, 0)
        
        if in_range:
            lcd.lcd_display_string("Seeker Nearby              ", 2, 0)
        else:
            lcd.lcd_display_string("Safe                       ", 2, 0)

        xbee.send(json.dumps(coords), XBeeAddress.P)

        
    
    