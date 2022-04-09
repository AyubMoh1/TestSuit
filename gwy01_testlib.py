import os


class GwyPower:
    def __init__(self, device):
        print('Setup power control here')
        
    def on(self):
        print('Power on here')

    def off(self):
        print('Power off here')

    def reboot(self):
        os.system("./power {device} off")
        os.system("./power {device} on")

class GwySerial:
    def __init__(self, serial_port):
        print('Setup serial here, 115200 8N1')

    def send_cmd(self, cmd)
        print('Send command over serial, e.g. cat /etc/sw_versions')

    def wait_for_row(self, row_start_str, timeout_s)
        print('Return row starting with row_start_str')
        res = True # not timeout
        res_str = ''
        return (res, res_str)
