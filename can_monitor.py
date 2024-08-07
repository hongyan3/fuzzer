import time
import threading

class CanMonitor(threading.Thread):
    def __init__(self, can_interface, name=None):
        threading.Thread.__init__(self,name=name)
        self.__can=can_interface
    
    def run(self):
        while True:
            try:
                id, data, timestamp = self.__can.receive_message(timeout=1)
                print('id: {},\tdata: {},\t,timestamp: {}'.format(hex(id),[hex(i) for i in data],timestamp), timestamp)
            except AttributeError as e:
                print('Receiving message timeout.')
            