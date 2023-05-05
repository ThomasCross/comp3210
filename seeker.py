from comp3210.helpers.gps import GPS
from comp3210.helpers.lcd import LCD
from comp3210.helpers.xbee import Xbee, XbeeListener, XBeeAddress
import time
import json
from math import cos, asin, sqrt, pi

gps = GPS()
lcd = LCD()
xbee = Xbee()

def distance(runner, seeker):
    p = pi/180
    a = 0.5 - cos((seeker[0]-runner[0])*p)/2 + cos(runner[0]*p) * cos(seeker[0]*p) * (1-cos((seeker[1]-runner[1])*p))/2
    return 12742 * asin(sqrt(a)) * 1000

# Update screen with range
def update_screen(address, message):
    runner_coords = json.loads(message)
    runner_coords = [float(runner_coords[0]), float(runner_coords[1])]

    lat, long = gps.get_gps()
    seeker_coords = [float(lat), float(long)]

    distance_to = distance(runner_coords, seeker_coords)

    if distance_to < 50:
        xbee.send('1', XBeeAddress.P)

        lcd.lcd_display_string("Distance2Runner         ", 1, 0)
        lcd.lcd_display_string(" <= 50m                  ", 2, 0)

    else:
        xbee.send('0', XBeeAddress.P)

        lcd.lcd_display_string("Distance2Runner         ", 1, 0)
        lcd.lcd_display_string("{:.1f}m                      ".format(distance_to), 2, 0)
    
    print("{:.1f}m".format(distance_to))

# Get GPS Lock
wait = 0
while True:
    lat, long = gps.get_gps()
    print("{}, {}".format(lat, long))

    if lat != None:
        break
    else:
        wait += 1
        lcd.lcd_display_string("Wait GPS connect             ", 1, 0)
        lcd.lcd_display_string("{}                           ".format(wait), 2, 0)
        time.sleep(1)

lcd.lcd_display_string("Awaiting runner         ", 1, 0)
lcd.lcd_display_string("GPS coordinates         ", 2, 0)

# Setup XBee
listener = XbeeListener(update_screen)
xbee.add_listener(listener)

while True:
    time.sleep(1)