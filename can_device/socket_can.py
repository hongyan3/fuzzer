import can
from can_abstract import CanInterface


class SocketCan(CanInterface):
    def __init__(self, channel, interface, bitrate=None):
        self.__send_bus = None
        self.__recv_bus = None
        self.__channel = channel
        self.__interface = interface
        self.__bitrate = bitrate

    def connect(self):
        try:
            self.__send_bus = can.interface.Bus(
                channel=self.__channel,
                interface=self.__interface,
                bitrate=self.__bitrate
            )
            self.__recv_bus = can.interface.Bus(
                channel=self.__channel,
                interface=self.__interface,
                bitrate=self.__bitrate
            )
            print('Can connection successed.')
        except can.CanError:
            print('Can not connect socket can.')
            exit(-1)

    def close(self):
        self.__send_bus.shutdown()
        self.__recv_bus.shutdown()
        pass

    def send_message(self, message_id, data, timestamp=None):
        msg = can.Message(arbitration_id=message_id, data=data, timestamp=timestamp)
        self.__send_bus.send(msg)

    def receive_message(self, timeout=None) -> (str, list, float):
        if timeout is None:
            msg = self.__recv_bus.recv()
        else:
            msg = self.__recv_bus.recv(timeout)
        return msg.arbitration_id, msg.data, msg.timestamp
