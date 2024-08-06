import cantools.database

from dbc_parser import DbcParser


class CanFuzzer:
    def __init__(self, file_path):
        parser = DbcParser(file_path)
        self.__messages = parser.parse_dbc_file()

    def generate_random_message(self, can_interface, message_id):
        """
        随机Fuzz

        :return:
        """
        pass

    def generate_order_message(self, can_interface, message_id):
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
            start = sig.start - sig.length + 1
            end = sig.start
            for i in range(2 ** sig.length):
                data_map = ['0' for _ in range(64)]
                data = []
                bin_str = format(i, '0{}b'.format(sig.length))
                bin_list = [i for i in bin_str]
                data_map[start:end + 1] = bin_list
                for j in range(0, 64, 8):
                    temp = data_map[j:j + 8]
                    temp = temp[::-1]
                    res = ''.join(temp)
                    data.append(int(res, 2))
                can_interface.send_message(message_id, data)
                print([hex(i) for i in data])

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
            print(temp[::-1])
        print()
