from fuzzer import CanFuzzer
from can_device import SocketCan, TosunCan


def main():
    dbc_file_path = r'C:\Users\LENOVO\Desktop\DBC\PreZSDB123500_DC1E_A2_L2_One_Motor_800V_Prvt_Propulsion_CAN_230821.dbc'
    ts_can = TosunCan()
    ts_can.connect()
    fuzzer = CanFuzzer(can_interface=ts_can)
    fuzzer.order_message_fuzz(dbc_file_path=dbc_file_path, duration=0.1)
    while True:
        pass


if __name__ == '__main__':
    main()
