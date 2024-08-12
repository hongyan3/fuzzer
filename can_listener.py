import threading
import time
import requests

"""
CAN 报文监视器
"""

WEB_HOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0999c60d-91b4-4a34-b012-d8f2d54451c8'


def send_web_msg(msg):
    data = {
        'msgtype': 'text',
        'text': {
            'content': msg
        }
    }
    requests.post(url=WEB_HOOK, json=data)


class CanListener:
    def __init__(self, can_interface):
        self.bus = can_interface
        self.last_message_time = None
        self.is_alive = True

    def send_activation(self, duration):
        """
        定期发送激活指令
        :param duration: 发送间隔
        :return:
        """
        msg_id = 0x512
        data = [0x15, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        while self.is_alive:
            try:
                self.bus.send_message(msg_id, data)
            except Exception as e:
                print("Send activation failed: {}".format(e))
            time.sleep(duration)

    def listen_for_message(self, timeout):
        """
        监听CAN总线消息
        :param timeout: 超时时间
        :return:
        """
        while self.is_alive:
            try:
                self.bus.receive_message(timeout)
            except TimeoutError:
                self.is_alive = False
                send_web_msg('fuzz程序超时')
                print('Receiving CAN message timed out.Time: {}'.format(time.time()))

    def start(self):
        """
        启动监听机制
        :return:
        """
        send_thread = threading.Thread(target=self.send_activation, args=(1,))
        listen_thread = threading.Thread(target=self.listen_for_message, args=(0.5,))

        send_thread.start()
        listen_thread.start()
