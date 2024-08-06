from fuzzer import CanFuzzer
from can_device import SocketCan


def main():
    can_fuzzer = CanFuzzer(r'C:\Users\LENOVO\Desktop\DBC\PreZSDB123500_CX1E_EU_800V_BodyCAN_230821.dbc')
    bus = SocketCan(channel='vcan0', interface='socketcan', bitrate=5000000)
    bus.connect()
    can_fuzzer.generate_order_message(can_interface=bus, message_id=0x121)


if __name__ == '__main__':
    main()
