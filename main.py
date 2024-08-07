from fuzzer import CanFuzzer
from can_device import SocketCan


def main():
    can_fuzzer = CanFuzzer(r'C:\Users\LENOVO\Desktop\DBC\PreZSDB123500_CX1E_EU_800V_PropulsionCAN_230821.dbc')
    bus = SocketCan(channel='vcan0', interface='socketcan', bitrate=5000000)
    # bus.connect()
    can_fuzzer.order_message_fuzz(can_interface=bus, message_id=0x159, duration=0.5)


if __name__ == '__main__':
    main()
