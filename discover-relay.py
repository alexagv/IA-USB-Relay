import argparse
import serial

# Create the parser
parser = argparse.ArgumentParser(description='Find the ID of a USB Intelligent\
                                              Appliance relay board')

# Add the arguments
parser.add_argument('-d',
                    '--device',
                    metavar='device',
                    type=str,
                    help='path to the USB device (default is /dev/ttyUSB0)',
                    default="/dev/ttyUSB0")

parser.add_argument('-b',
                    '--baudrate',
                    metavar='baudrate',
                    type=int,
                    help='baudrate for the relay (default 19200)',
                    default=19200)

args = parser.parse_args()

try:
    ser = serial.Serial(args.device, args.baudrate, timeout=5)
    # The relay can have a unique address between 0-255 in hex
    for i in range(0, 255):
        command = "?{:02x}0\r".format(i).upper()
        print("Sending command: ", command)
        ser.write(command.encode())
        response = ser.readline()
        if response.decode().startswith("_"):
            print("Found relay with model ID:", response.decode().strip("_"))
            print("Address: "+"{:02x}".format(i).upper())
            break
except Exception as e:
    print(e)
finally:
    ser.close()
