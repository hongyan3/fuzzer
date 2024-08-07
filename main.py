from fuzzer import CanFuzzer
from can_device import SocketCan


def main():
    can_fuzzer = CanFuzzer(r'C:\Users\LENOVO\Desktop\DBC\PreZSDB123500_CX1E_EU_800V_PropulsionCAN_230821.dbc')
    bus = SocketCan(channel='vcan0', interface='socketcan', bitrate=5000000)
    # bus.connect()
    can_fuzzer.generate_order_message(can_interface=bus, message_id=0x159)


def range_index(start, length) -> (int, int):
    group = start // 8
    index_group = start % 8
    left = group * 8 + (7 - index_group)
    right = left + length - 1
    return left, right


if __name__ == '__main__':
    main()
    # print(range_index(39, 4))
