import random
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

    def random_message_fuzz(self, duration=None):
        """
        随机Fuzz

        :return:
        """
        while True:
            msg_id = self.get_random_message_id()
            data = self.get_random_data()
            self.__bus.send_message(msg_id, data)
            if duration is not None:
                time.sleep(duration)
            # self.write_file('id: {}, data: {}, timestamp: {}'.format(hex(msg_id), ['0x' + hex(i)[2:].zfill(2) for i in data],
            #                                                          time.time()))

    @staticmethod
    def get_random_message_id():
        msg_id = random.randint(0x0, 0x7FF)
        return msg_id

    @staticmethod
    def get_random_data():
        data_length = random.randint(1, 8)
        data = [0] * 8
        for _ in range(data_length):
            index = random.randint(0, 7)
            while data[index] != 0:
                index = random.randint(0, 7)
            data_byte = random.randint(0, 0xFF)
            data[index] = data_byte
        return data

    def order_message_fuzz(self, dbc_file_path, duration=None):
        """
        顺序Fuzz

        :param dbc_file_path: dbc文件路径
        :param duration: 间隔时间
        :return:
        """
        dbc = DBCLoader(dbc_file_path)
        # 开启心跳检测
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

    @staticmethod
    def __range_index(start, length) -> (int, int):
        group = start // 8
        index_group = start % 8
        left = group * 8 + (7 - index_group)
        right = left + length - 1
        return left, right

    @staticmethod
    def __signal_matrix(data):
        for i in range(0, len(data), 8):
            temp = data[i:i + 8]
            print(temp)
        print('')

    @staticmethod
    def write_file(msg):
        with open('fuzz.log', 'w') as f:
            f.write(msg)
            f.write('\n')