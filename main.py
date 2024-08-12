from can_listener import CanListener
from fuzzer import CanFuzzer
from can_device import SocketCan, TosunCan


def main():
    ts_can = TosunCan()
    ts_can.connect()
    # 开启监听
    listener = CanListener(can_interface=ts_can)
    listener.start()
    # 开启fuzz
    fuzzer = CanFuzzer(can_interface=ts_can)
    fuzzer.random_message_fuzz(duration=0.001)


if __name__ == '__main__':
    main()