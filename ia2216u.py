import serial


class Relay(object):
    def __init__(self, device, baudrate=19700, id="00"):
        self.id = str(id).upper()  # hexadecimal address of the device
        self.ser = serial.Serial(device, baudrate, timeout=5)

    def openRelay(self, relay_nr):
        return self.__setCommand(relay_nr, command=3)  # 3 = Relay activation

    def closeRelay(self, relay_nr):
        return self.__setCommand(relay_nr, command=4)  # 4 = Relay deactivation

    def getStatus(self, relay_nr):
        response = self.__getCommand(command=2)  # 2 = Read IO status
        if response:
            if len(response) == 5:
                binary_status_list = self.__hexNibbleToBinary(response)
                index = len(binary_status_list) - relay_nr  # list is backwards
                if int(binary_status_list[index]):  # int to make it boolean
                    return 1
                else:
                    return 0
        else:
            return -1

    def __hexNibbleToBinary(self, hexdata):
        scale = 16  # base number for hexadecimal
        num_of_bits = 16  # board is 16 channels
        return bin(int(hexdata, scale))[2:].zfill(num_of_bits)

    def __setCommand(self, relay_nr, command):
        try:
            if relay_nr <= 0 or not isinstance(relay_nr, int):
                return False
            zero_index_nr = relay_nr-1
            command_str = "!"+self.id+str(command)+\
                          "{:02x}0\r".format(zero_index_nr).upper()
            self.ser.write(command_str.encode())
            response = self.ser.readline()
            if response.decode().startswith("|"):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def __getCommand(self, command):
        try:
            command_str = "?"+self.id+str(command)+"\r"
            self.ser.write(command_str.encode())
            response = self.ser.readline()
            if response.decode().startswith("_"):
                return response.decode().split("_")[-1]
            else:
                return False
        except Exception as e:
            print(e)
            return False


def main():
    device = "/dev/ttyUSB2"
    baudrate = 19200  # default for the boards
    board_address = "00"  # internal board address in hex
    relay = Relay(device, baudrate, board_address)
    relay_nr = 5  # the relay we want to control (one based index)
    print("Testing relay %s on the device attached to:" % relay_nr, device)
    print("Open relay %s:" % relay_nr, relay.openRelay(5))
    print("Relay %s status:" % relay_nr, relay.getStatus(5))
    print("Closing relay %s:" % relay_nr, relay.closeRelay(5))
    print("Relay %s status:" % relay_nr, relay.getStatus(5))


if __name__ == '__main__':
    main()
