from comp3210.helpers.gps import GPS
from comp3210.helpers.lcd import LCD
from comp3210.helpers.xbee import Xbee, XbeeListener, XBeeAddress
import time
import json
from math import cos, asin, sqrt, pi

gps = GPS()
lcd = LCD()
#xbee = Xbee()



def distance(runner, seeker):
    p = pi/180
    a = 0.5 - cos((seeker['lat']-runner['lat'])*p)/2 + cos(runner['lat']*p) * cos(seeker['lat']*p) * (1-cos((seeker['long']-runner['long'])*p))/2
    return 12742 * asin(sqrt(a)) * 1000

# Update screen with range
def update_screen(address, message):
    runner_coords = json.loads(message)
    
    lat, long = gps.get_lat_long()
    seeker_coords = {
        "lat": float(lat),
        "long": float(long)
    }

    distance_to = distance(runner_coords, seeker_coords)

    lcd.lcd_display_string("Distance>Runner         ", 1, 0)
    lcd.lcd_display_string("{:.1f}m                      ".format(distance_to), 2, 0)
    print("{:.1f}m".format(distance_to))

# Get GPS Lock
wait = 0
while True:
    lat, long = gps.get_lat_long()
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

runner_coords = {
    "lat": float(51.348190),
    "long": float(-0.204196)
}
update_screen("", json.dumps(runner_coords))

input()

# Setup XBee
listener = XbeeListener(update_screen)
#xbee.add_listener(listener)

