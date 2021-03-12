import can
import os
import time
from threading import Thread

#_canIdTank123 = "cff3d17"
_canIdTank123 = "14ff0221"
_canIdTank456 = "cff4017"
_canIdNira3 = "cff3e17"
_canIdWheelSpeed = "18fef100"

tempList = []
pressureList = []

def msg_receiving():
    print('msg_receiving')
    outDir = "Display_rep/out/hydraFL"  # "/home/pi/rough/logger-rbp-python-out/lomack150_"
    numCAN = 1  # 2
    bRate = 250000  # 250000 or 500000
    CANtype = "RBP15"  # OCAN or ACAN
    numTank = 5
    volumeStr = "202,202,202,202,148"

    volumeL = [float(x) for x in volumeStr.split(",")]

    os.system("sudo /sbin/ip link set can0 down")
    if numCAN == 2:
        os.system("sudo /sbin/ip link set can1 down")

    # Make CAN interface to 250 or 500kbps
    setCANbaudRate(numCAN, bRate)

    # Connect to Bus
    bus0 = connectToLogger('can0')

    # Continually recieved messages
    #readwriteMessageThread(bus0)
    can_rx_task(bus0)
    # if numCAN == 2:
    #    readwriteMessageThread(bus1, outDir, numCAN, bRate, CANtype + "1", numTank, volumeL)

    # Continually write readMessages
    try:
        while True:
            pass

    except KeyboardInterrupt:
        # Catch keyboard interrupt
        os.system("sudo /sbin/ip link set can0 down")
        exit()


def setCANbaudRate(numCAN, bRate):
    print('setCANbaudRate')
    """
    Make CAN interface to 250 or 500 kbps
    """
    os.system("sudo /sbin/ip link set can0 up type can bitrate " + str(bRate))
    if numCAN == 2:
        os.system("sudo /sbin/ip link set can1 up type can bitrate " + str(bRate))
    time.sleep(0.1)


def connectToLogger(canV):
    print('connectToLogger')
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
    print('readWrite')
    """
    In seperate thread continually recieve messages from CAN logger
    """
    # Start receive thread
    t = Thread(target=can_rx_task, args=bus)
    t.start()


def liveUpdateTruck(outstr):
    #print('liveupdate')
    tempL = []
    pressures = []

    splt = outstr.strip().split(" ")

    # date, can ID, hex value
    if (outstr[0] != "*"):
        try:
            #print('nice')
            idV = splt[3].lower()[2:]
            hexVsplt = splt[6:]
            hexV = ""
            for h in hexVsplt:
                if len(h) == 1:
                    hexV += "0" + h
                elif len(h) == 2:
                    hexV += h
        except IndexError:
            hexV = ""
            idV = ""

        if len(hexV) == 16:
            #print('lengthgood')

            #######################################################################################
            # Temperature and Pressure T1-T3
            if (idV == _canIdTank123):
                print('tank123msgfound')

                pressures[0] = (enforceMaxV(((int(hexV[0:2], 16)) + ((int(hexV[2:4], 16) & 0b00001111) << 8)), 4015) * 0.1)
                presT2 = (enforceMaxV((((int(hexV[2:4], 16) & 0b11110000) >> 4) + ((int(hexV[4:6], 16)) << 4)), 4015) * 0.1)
                tempL[0] = (enforceMaxV(((int(hexV[10:12], 16))), 250) * 1.0) - 40.0
                tempL[1] = (enforceMaxV(((int(hexV[12:14], 16))), 250) * 1.0) - 40.0
                tempL[2] = (enforceMaxV(((int(hexV[14:16], 16))), 250) * 1.0) - 40.0



            #######################################################################################
            # Temperature T4-T6
            elif (idV == _canIdTank456):
                print('tank456msgfound')
                tempL[3] = (enforceMaxV(((int(hexV[10:12], 16))), 250) * 1.0) - 40.0
                tempL[4] = (enforceMaxV(((int(hexV[12:14], 16))), 250) * 1.0) - 40.0
                tempL[5] = (enforceMaxV(((int(hexV[14:16], 16))), 250) * 1.0) - 40.0


                #print(tempL)

            #######################################################################################
            # Rail pressure
            elif (idV == _canIdNira3):
                print('nira3')
                pressures[1] = (enforceMaxV(((int(hexV[12:14], 16))), 4015) * 0.1)




            #######################################################################################

    return (pressures, tempL)


def createLogLine(message):
    #print('createlogline')

    hmsfV = 'placeholder:'

    # PGN
    pgnV = '0x{:02x}'.format(message.arbitration_id)

    # Hex
    hexV = ''
    for i in range(message.dlc):
        hexV += '{0:x} '.format(message.data[i])

    outstr = " ".join([hmsfV, "Rx", "1", pgnV, "x", str(message.dlc), hexV]) + " "

    print(outstr)

    return (outstr)


def can_rx_task(bus):
    print('can_rx_task')
    tempL = []
    pressureL = []

    while True:
        # recieve message and extract info
        (outstr) = createLogLine(bus.recv())

        (tempL, pressureL) = liveUpdateTruck(outstr)

        #print(tempL)


def enforceMaxV(origV, maxV):
    """
    ...
    """
    if origV < maxV:
        return origV
    else:
        return maxV


if __name__ == '__main__':
    msg_receiving()