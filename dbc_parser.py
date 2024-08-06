import cantools


class DbcParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.messages = {}

    def parse_dbc_file(self) -> []:
        """
        解析dbc文件并填充到messages列表

        :return:
        """
        dbc = cantools.db.load_file(self.file_path)
        self.messages = dbc.messages
        return self.messages
