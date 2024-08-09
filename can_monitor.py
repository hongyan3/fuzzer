import threading

"""
CAN 报文监视器
"""


class CanMonitor(threading.Thread):
    def __init__(self, can_interface, name=None, daemon=False):
        threading.Thread.__init__(self, name=name)
        threading.Thread.daemon = daemon
        self.__can = can_interface

    def run(self):
        while True:
            try:
                msg_id, data, timestamp = self.__can.receive_message(timeout=1)
                print('id: {},\tdata: {},\t,timestamp: {}'.format(hex(msg_id), [f'0x{i:02x}' for i in data], timestamp))
            except AttributeError as e:
                print('Receiving message failed. {}'.format(e))
