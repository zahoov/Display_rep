import os
import can
from threading import Thread

display_code_dir = 'ENTER WHERE ITS SAVING TO'


def main():

    bRate = 9600

    os.system("sudo /sbin/ip link set can0 down")

    # Make CAN interface to 250 or 500kbps
    setCANbaudRate(bRate)

    # Connect to Bus
    bus0 = connectToLogger('can0')

    # Continually recieved messages
    readwriteMessageThread(bus0)

    # Continually write readMessages
    try:
        while True:
            pass

    except KeyboardInterrupt:
        # Catch keyboard interrupt
        os.system("sudo /sbin/ip link set can0 down")


def setCANbaudRate(bRate):
    """
    Make CAN interface to 250 or 500 kbps
    """
    os.system("sudo /sbin/ip link set can0 up type can bitrate " + str(bRate))


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


def readwriteMessageThread(bus):
    """
    In seperate thread continually recieve messages from CAN logger
    """
    # Start receive thread
    t = Thread(target=can_rx_task, args=bus)
    t.start()


def createLogLine(message):
    """
    Format the CAN message
    """

    if os.path.isfile(display_code_dir + "J1587_log.txt"):
        fin = open(display_code_dir + "J1587_log.txt", "r+")
        fin.write(message)
        fin.close()
        print(message)

    else:
        fin = open(display_code_dir + "J1587_log.txt", "w")
        fin.write(message)
        fin.close()
        print(message)


def can_rx_task(bus):
    while True:
        createLogLine(bus.recv())


if __name__ == '__main__':
    main()
