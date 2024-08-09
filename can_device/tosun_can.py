import time

from libTSCANAPI import *
from ctypes import c_bool, c_size_t, c_char_p
from can_abstract import CanInterface

PREFIX = '[TOSUN]'


class TosunCan(CanInterface):
    def __init__(self, serial_number=None):
        """
        同星CAN盒初始化

        :param serial_number: 产品序列号，若电脑只连接一个设备可省略该参数
        """
        self.__can = c_size_t(0)
        if serial_number is not None:
            self.__device_code = serial_number.encode()
        else:
            self.__device_code = b''
        initialize_lib_tscan(True, True, False)

    def connect(self):
        """
        连接同星设备
        :return:
        """
        code = tsapp_connect(self.__device_code, self.__can)
        if code == 0:
            print(f'{PREFIX} Device connection successful. handle: {self.__can.value}.')
            # 设置波特率
            tsapp_configure_baudrate_can(self.__can, 0, 500, 1)
            tsapp_configure_baudrate_can(self.__can, 1, 500, 1)
        elif code == 5:
            print(f'{PREFIX} Device is already connected.')
        else:
            msg = self.__get_error_description(code)
            print(f'{PREFIX} Device connection failed, error code: {code}, msg: {msg.value.decode()}')
            exit(-1)

    def close(self):
        tsapp_disconnect_by_handle(self.__can)
        finalize_lib_tscan()

    def send_message(self, message_id, data, timestamp=None):
        message = TLIBCAN(
            FIdxChn=0,
            FDLC=8,
            FIdentifier=message_id,
            FProperties=1,
            FData=data
        )
        res = tsapp_transmit_can_async(self.__can, message)
        if res != 0:
            msg = self.__get_error_description(res)
            print(f'Message send failed, msg: {msg.value.decode()}')
            return

    def receive_message(self, timeout=None) -> (str, list, float):
        start_time = time.time()
        while True:
            buffer = (TLIBCANFD * 1)()
            buff_size = s32(1)
            tsfifo_receive_canfd_msgs(self.__can, buffer, buff_size, 0, READ_TX_RX_DEF.ONLY_RX_MESSAGES)
            msg = buffer[0]
            end_time = time.time()
            if buff_size.value > 0 and msg.FIdentifier > 0:
                break
            if (timeout is not None) and (end_time - start_time > timeout):
                raise TimeoutError
        msg_id = msg.FIdentifier
        data = []
        timestamp = msg.FTimeUs
        for i in range(DLC_DATA_BYTE_CNT[msg.FDLC]):
            data.append(msg.FData[i])
        return msg_id, data, timestamp

    @staticmethod
    def __get_error_description(code):
        """
        根据错误码获取描述
        :param code: 错误码
        :return:
        """
        result = c_char_p()
        tscan_get_error_description(code, result)
        return result
