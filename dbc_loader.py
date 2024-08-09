import cantools


class DBCLoader:
    def __init__(self, file_path):
        self.__dbc = cantools.db.load_file(file_path)

    def messages(self) -> []:
        """
        解析dbc文件并填充到messages列表

        :return:
        """
        return self.__dbc.messages

    def get_message_by_id(self, msg_id):
        """
        根据报文id获取报文实例
        :param msg_id: 报文id
        :return:
        """
        for msg in self.messages():
            if msg.frame_id == msg_id:
                return msg