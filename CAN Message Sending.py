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


def can_rx_task(bus, fin):

    while True:
        # recieve message and extract info
        outstr = createLogLine(bus.recv())

        fin.write(outstr)





def readwriteMessageThread(bus, outDir):
    """
    In seperate thread continually recieve messages from CAN logger
    """
    # Start receive thread
    t = Thread(target=can_rx_task, args=(bus, outDir))
    t.start()


def createLogLine(message):

    # PGN
    pgnV = '0x{:02x}'.format(message.arbitration_id)

    # Hex
    hexV = ''
    for i in range(message.dlc):
        hexV += '{0:x} '.format(message.data[i])

    outstr = " ".join([time.strftime("%d_%H_%M_%S"), "Rx", "1", pgnV, "x", str(message.dlc), hexV]) + " "

    return outstr


def main():
    outDir = open("Display_rep/CAN2_TEST.txt", 'w')
    numCAN = 1
    bRate = 250000

    os.system("sudo /sbin/ip link set can0 down")
    if numCAN == 2:
        os.system("sudo /sbin/ip link set can1 down")

    # Make CAN interface to 250 or 500kbps
    setCANbaudRate(numCAN, bRate)

    # Connect to Bus
    bus0 = connectToLogger('can0')

    # Continually recieved messages
    readwriteMessageThread(bus0, outDir)

    # Continually write readMessages
    try:
        while True:
            pass

    except KeyboardInterrupt:
        # Catch keyboard interrupt
        os.system("sudo /sbin/ip link set can0 down")


if __name__ == "__main__":
    main()
