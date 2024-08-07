from abc import ABC, abstractmethod


class CanInterface(ABC):
    @abstractmethod
    def connect(self):
        """建立CAN总线的连接"""
        pass

    @abstractmethod
    def close(self):
        """关闭CAN接口连接"""
        pass

    @abstractmethod
    def send_message(self, message_id, data, timestamp=None):
        """
        发送一条CAN消息

        :param message_id 消息ID
        :param data: 要发送的数据
        :param timestamp: 可选时间戳
        :return:
        """
        pass

    @abstractmethod
    def receive_message(self, timeout=None) -> (str, list, float):
        """
        接收CAN消息

        :return: 返回接收到的消息元组 (message_id, data, timestamp)
        """
        pass
