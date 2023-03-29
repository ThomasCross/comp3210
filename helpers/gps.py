import time
import board
import serial

import adafruit_gps

class GPS:
    def __init__():
        RX = board.RX
        TX = board.TX

        uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

        self.__gps = adafruit_gps.GPS(uart, debug=False)

        self.__gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        self.__gps.send_command(b'PMTK220,1000')

    def get_lat_long():
        self.__gps.update()

        return self.__gps.latitude, self.__gps.longitude
