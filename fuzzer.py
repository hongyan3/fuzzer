import time

import cantools.database

from dbc_parser import DbcParser


class CanFuzzer:
    def __init__(self, file_path):
        parser = DbcParser(file_path)
        self.__messages = parser.parse_dbc_file()

    def random_message_fuzz(self, can_interface, message_id):
        """
        随机Fuzz

        :return:
        """
        pass

    def order_message_fuzz(self, can_interface, message_id, duration=None):
        """
        顺序Fuzz

        :return:
        """
        message = None
        for msg in self.__messages:
            if msg.frame_id == message_id:
                message = msg
                break
        if message is None:
            print('Not found message by this id.')
            return
        for sig in message.signals:
            print('Start fuzzing with {}...'.format(sig.name))
            start, end = self.__range_index(sig.start, sig.length)
            for i in range(2 ** sig.length):
                data_map = ['0'] * 64
                data = []
                bin_str = format(i, '0{}b'.format(sig.length))
                bin_list = [i for i in bin_str]
                data_map[start:end + 1] = bin_list
                for j in range(0, 64, 8):
                    temp = data_map[j:j + 8]
                    res = ''.join(temp)
                    data.append(int(res, 2))
                if duration is not None:
                    time.sleep(duration)
                # self.send_message(can_interface, message_id, data)
                print(['0x'+hex(i)[2:].zfill(2) for i in data])  # 打印Hex类型的data

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
