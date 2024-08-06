import can
from can_abstract import CanInterface


class SocketCan(CanInterface):
    def __init__(self, channel, interface, bitrate=None):
        self.__bus = None
        self.__channel = channel
        self.__interface = interface
        self.__bitrate = bitrate

    def connect(self):
        try:
            self.__bus = can.interface.Bus(
                channel=self.__channel,
                interface=self.__interface,
                bitrate=self.__bitrate
            )
        except can.CanError:
            print('Can not connect socket can.')

    def close(self):
        self.__bus.shutdown()
        pass

    def send_message(self, message_id, data, timestamp=None):
        msg = can.Message(arbitration_id=message_id, data=data, timestamp=timestamp)
        self.__bus.send(msg)

    def receive_message(self) -> (str, list, float):
        pass
