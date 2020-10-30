import can
import time
import os
from threading import Thread


def setCANbaudRate(numCAN, bRate):
    """
    Make CAN interface to 250 or 500 kbps
    """
    os.system("sudo /sbin/ip link set can0 up type can bitrate " + str(bRate))
    if numCAN == 2:
        os.system("sudo /sbin/ip link set can1 up type can bitrate " + str(bRate))
    time.sleep(0.1)


def connectToLogger(canV):
    """
    Connect to Bus
    """
    try:
        bus = can.interface.Bus(channel=canV, bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()
    return bus


def can_rx_task(bus, fin, baudrate):
    now = time.strftime("%M%S")
    i = 0
    while i < 5:

        # recieve message and extract info
        outstr = createLogLine(bus.recv(timeout=1), baudrate)
        print(outstr)
        fin.write(outstr)
        i += 1



def createLogLine(message, baudrate):
    # PGN
    pgnV = '0x{:02x}'.format(message.arbitration_id)

    # Hex
    hexV = ''
    for i in range(message.dlc):
        hexV += '{0:x} '.format(message.data[i])

    outstr = " ".join([time.strftime("%d_%H_%M_%S"), baudrate, pgnV, "x", str(message.dlc), hexV]) + " "

    return outstr


def main():
    outDir = open("Display_rep/CAN2_TEST.txt", 'w')
    numCAN = 1
    # bRate = 250000
    testing = True
    i = 0

    mode = input('mode 1 for baudrates, mode 2 for 1000 increments')

    bRate = 0
    baudrates = [9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000, 667000]

    while testing:

        if mode == 1:
            bRate = baudrates[i]
        else:
            bRate = bRate + 10000


        os.system("sudo /sbin/ip link set can0 down")
        if numCAN == 2:
            os.system("sudo /sbin/ip link set can1 down")

        # Make CAN interface to 250 or 500kbps
        setCANbaudRate(numCAN, bRate)

        # Connect to Bus
        bus0 = connectToLogger('can0')

        # Continually recieved messages
        can_rx_task(bus0, outDir, bRate)

        i += 1

        if i == 8:
            testing = False


if __name__ == "__main__":
    main()
