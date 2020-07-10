# IA-USB-Relay
Simple python tools to interface with the IA USB relay boards.

## Dependencies
Depends on PySerial

`pip install pyserial`

## IA2216U.py
Python module to interface with the Intelligent Appliance [IA-2216-U](https://www.intelligent-appliance.com/images/IA-2216-U-UM-V0418.pdf) USB relay boards.

## discover-relay.py
CLI tool to figure out the device internal address which can be set to 256 different HEX addresses, given you know which USB port the board is attached to. Default baudrate for these boards is 19200.
### Example usage:
```
python3 discover-relay.py -d "/dev/ttyUSB2" -b "19200"
```
