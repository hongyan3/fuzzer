import threading
import time

from dbc_loader import DBCLoader

"""
CAN Fuzz 模糊测试

包括全随机测试（无规则）、单信号顺序测试、信号随机测试（依据信号规则）
"""


class CanFuzzer:
    def __init__(self, can_interface):
        self.__bus = can_interface

    def random_message_fuzz(self, can_interface, message_id):
        """
        随机Fuzz

        :return:
        """
        pass

    def order_message_fuzz(self, dbc_file_path, duration=None):
        """
        顺序Fuzz

        :param dbc_file_path: dbc文件路径
        :param duration: 间隔时间
        :return:
        """
        dbc = DBCLoader(dbc_file_path)
        # 开启心跳检测
        self.health_check(0x512, [0x15, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], 0.2)
        for msg in dbc.messages():
            print('Start fuzzing the message: {}, name: {}.'.format(f'0x{msg.frame_id:02x}', msg.name))
            for sig in msg.signals:
                print('Start fuzzing the signal: {}.'.format(sig.name))
                start, end = self.__range_index(sig.start, sig.length)
                for i in range(2 ** sig.length):
                    # 生成bitmap并填充
                    data_map = ['0'] * 64
                    data = []
                    # 生成当前信号长度的二进制字符串
                    bin_str = format(i, '0{}b'.format(sig.length))
                    bin_list = [i for i in bin_str]
                    # 替换bitmap中对应信号的数据
                    data_map[start:end + 1] = bin_list
                    for j in range(0, 64, 8):
                        temp = data_map[j:j + 8]
                        res = ''.join(temp)
                        data.append(int(res, 2))
                    if duration is not None:
                        time.sleep(duration)
                    self.__bus.send_message(msg.frame_id, data)
                    # print(['0x' + hex(i)[2:].zfill(2) for i in data])  # 打印Hex类型的data

    def health_check(self, msg_id, data, duration, timeout=0.1):
        def run():
            print('Start health checking progress.')
            while True:
                try:
                    self.__bus.send_message(msg_id, data)
                    self.__bus.receive_message(timeout)
                except TimeoutError:
                    print('Health check timeout, current timestamp: {}.'.format(time.time()))
                    exit(-1)
                time.sleep(duration)
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    @staticmethod
    def __range_index(start, length) -> (int, int):
        group = start // 8
        index_group = start % 8
        left = group * 8 + (7 - index_group)
        right = left + length - 1
        return left, right

    @staticmethod
    def send_message(can_interface, message_id, data):
        """
        使用CAN接口发送CAN消息

        :param can_interface: CAN接口
        :param message_id: 消息ID
        :param data: 要发送的数据
        :return:
        """
        can_interface.send_message(message_id, data)

    @staticmethod
    def __signal_matrix(data):
        for i in range(0, len(data), 8):
            temp = data[i:i + 8]
            print(temp)
        print('')
