from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from collections.abc import Callable
from enum import unique, Enum

class XbeeListener:
    # This class is used to create xbee receiving listeners

    def __init__(self, subject: Callable):
        self.__subject = subject

    def notify(self, address, message):
        self.__subject(address, message)

@unique
class XBeeAddress(str, Enum):
    # This class is an Enum used to identify XBees
    C = "0013A20041CF05CC"
    P = "0013A20041CF05EB"

class Xbee:
    # This class is used to send and receive data via the XBee

    def __init__(self):
        # Init XBee
        self.__xbee = XBeeDevice("/dev/ttyUSB1", 9600)
        self.__xbee.open()

        # Init Remote XBees
        self.__c = RemoteXBeeDevice(self.__xbee, XBee64BitAddress.from_hex_string("0013A20041CF05CC"))
        self.__p = RemoteXBeeDevice(self.__xbee, XBee64BitAddress.from_hex_string("0013A20041CF05EB"))

        # Add receiving
        self.__xbee.add_data_received_callback(self.__receive_data)
        self.__listeners = []

    def add_listener(self, listener: XbeeListener):
        # Add receiving listener
        self.__listeners.append(listener)

    def remove_listener(self, listener: XbeeListener):
        # Remove receiving listener
        self.__listeners.remove(listener)

    def notify(self, address, message):
        # Notify receiving listener
        for listener in self.__listeners:
            listener.notify(address, message)

    def __receive_data(self, xbee_message):
        # Receives xbee messages and forwards to notifier
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")

        self.notify(address, data)

    def send(self, message, remote: XBeeAddress):
        # Send message via XBee to remote XBee
        for i in range(1, 3):  # Retry 3 times
            try:
                address = XBee64BitAddress.from_hex_string(remote)

                if address == self.__c.get_64bit_addr():
                    self.__xbee.send_data(self.__c, message)

                elif address == self.__p.get_64bit_addr():
                    self.__xbee.send_data(self.__p, message)

                else:
                    print(
                        "XBee failed to send message ({}) to ({}) doesn't exist".format(
                            message,
                            remote
                        )
                    )
                    break

            except Exception as e:  # Log and Retry
                print(
                    "XBee failed to send message ({}) to ({}) Attempt {}: {}".format(
                        message,
                        remote,
                        i,  # Retry No.
                        e  # Exception Message
                    )
                )
                if i >= 3:  # Failed too many times
                    print("Failed to send message")

            else:  # Success break loop and continue
                break

    def close(self):
        # This closes the connection to the xbee
        self.__xbee.close()

xbee = Xbee()

xbee.send("Test message", XBeeAddress.P)
