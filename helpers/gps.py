import time
import serial
import threading

import adafruit_gps

class GPS:
    def __init__(self):
        uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

        self.__gps = adafruit_gps.GPS(uart, debug=False)

        self.__gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
        self.__gps.send_command(b'PMTK220,1000')

        self.__last = None, None

        self.__thread = threading.Thread(target=self.__thread, name='rgb_led')
        self.__thread.start()
        
    def __thread(self):
        while True:
            time.sleep(1)
            self.__gps.update()

            if not self.__gps.has_fix:
                self.__last = None, None
                
            else:
                self.__last = '{0:.6f}'.format(self.__gps.latitude), '{0:.6f}'.format(self.__gps.longitude)  

    def get_gps(self):
        return self.__last