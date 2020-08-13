#!/usr/bin/python3

# Hydra Energy
# 05/24/2019

import can
import time
import os
import queue
import sys
from threading import Thread
import zipfile

_canIdTank123 = "cff3d17"
_canIdTank456 = "cff4017"
_canIdNira3 = "cff3e17"
_canIdWheelSpeed = "18fef100"


def enforceMaxV(origV, maxV):
    """
    ...
    """
    if origV < maxV:
        return origV
    else:
        return maxV


def hydrogenMassEq2(pressureV, tempV, volumeV):
    """
    Calculate the hydrogen mass using more complex equation
    Value returns in unit kilo grams
    """

    var1 = 0.000000001348034
    var2 = 0.000000267013
    var3 = 0.00004247859
    var4 = 0.000001195678
    var5 = 0.0003204561
    var6 = 0.0867471

    component1 = (((-var1 * (tempV ** 2)) + (var2 * tempV) - var3) * (pressureV ** 2))
    component2 = ((var4 * (tempV ** 2)) - (var5 * tempV) + var6) * pressureV

    HmassTotal = (component1 + component2) * volumeV
    HmassTotalKg = HmassTotal / 1000.0
    return HmassTotalKg


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




def liveUpdateTruck(outstr, livefeedNiraErrorFname, livefeedHmassFname, prevNiraError, YDM,
                    tempL, curVarL, volumeL, numTank, maxNumTanks, prevSec):
    """
    ...
    """
    splt = outstr.strip().split(" ")

    # Timestamp with date
    monthNumToChar = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
                      9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    [dayV, monthV, yearV] = YDM[0].split(":")
    hmsStr = ":".join(YDM[1].split(":")[:3])
    outDate = " ".join([dayV, monthNumToChar[int(monthV)], yearV, hmsStr])

    [railPressure, presT1, wheelSpeed] = curVarL
    # date, can ID, hex value
    if (outstr[0] != "*"):
        try:
            dateV = splt[0]
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
            #######################################################################################
            # Nirai7LastFaultNumber_spnPropB_3E
            if (idV == _canIdNira3):
                dateCond0 = (len(splt[0]) != 12)
                dateCond1 = ((len(splt[0]) == 13) and (len(splt[0].split(":")[-1]) == 4))

                piCcond = ((len(hexV) != 16) or (dateCond0 and not (dateCond1)))

                if piCcond:
                    pass
                else:
                    nirai7LastFaultNumber = (enforceMaxV(((int(hexV[6:8], 16))), 255) * 1.0)

                    if prevNiraError == None:
                        prevNiraError = nirai7LastFaultNumber
                    elif nirai7LastFaultNumber != prevNiraError:

                        'INSERT CODE HERE'

            #######################################################################################
            # Temperature and Pressure T1-T3
            if (idV == _canIdTank123):
                presT1 = (enforceMaxV(((int(hexV[0:2], 16)) +
                                       ((int(hexV[2:4], 16) & 0b00001111) << 8)), 4015) * 0.1)
                presT2 = (enforceMaxV((((int(hexV[2:4], 16) & 0b11110000) >> 4) +
                                       ((int(hexV[4:6], 16)) << 4)), 4015) * 0.1)
                tempL[0] = (enforceMaxV(((int(hexV[10:12], 16))), 250) * 1.0) - 40.0
                tempL[1] = (enforceMaxV(((int(hexV[12:14], 16))), 250) * 1.0) - 40.0
                tempL[2] = (enforceMaxV(((int(hexV[14:16], 16))), 250) * 1.0) - 40.0

            #######################################################################################
            # Temperature and Pressure T4-T6
            elif (idV == _canIdTank456):
                tempL[3] = (enforceMaxV(((int(hexV[10:12], 16))), 250) * 1.0) - 40.0
                tempL[4] = (enforceMaxV(((int(hexV[12:14], 16))), 250) * 1.0) - 40.0
                tempL[5] = (enforceMaxV(((int(hexV[14:16], 16))), 250) * 1.0) - 40.0

            #######################################################################################
            # Rail pressure
            elif (idV == _canIdNira3):
                railPressure = (enforceMaxV(((int(hexV[12:14], 16))), 4015) * 0.1)

            #######################################################################################
            # Wheel-Based Vehicle Speed
            elif (idV == _canIdWheelSpeed):
                wheelSpeed = (enforceMaxV(((int(hexV[2:4], 16)) + ((int(hexV[4:6], 16)) << 8)),
                                          64259) * 0.003906)

            #######################################################################################
            # curHr = int(dateV.split(":")[1])
            # if ((curHr in [0, 15, 30, 45]) and (curHr != lastQuarterHour)):
            curSec = int(dateV.split(":")[2])
            if curSec != prevSec:
                ###################################################################################
                # H mass calculation
                HtotalMass = None
                if (not (None in tempL) and (presT1 != None)):
                    HtotalMassL = []
                    for t in range(numTank):
                        # Only consider tank 1 hydrogen pressure
                        currHtotalMassT = hydrogenMassEq2(presT1, tempL[t], volumeL[t])
                        HtotalMassL.append(currHtotalMassT)

                    HtotalMass = round(sum(HtotalMassL), 1)

                    'Insert code here'

                tempL = []
                for i in range(maxNumTanks): tempL.append(None)
                presT1 = None
                railPressure = None
                wheelSpeed = None

                prevSec = curSec
                # lastQuarterHour = curHr

    curVarL = [railPressure, presT1, wheelSpeed]

    return (prevNiraError, tempL, curVarL, prevSec)


def extractTimeFromEpoch(timeStamp):
    """
    Extract all the relative time and date info from CAN timestamp
    """
    ymdFV = time.strftime('%Y%m%d', time.localtime(timeStamp))
    ymdBV = time.strftime('%d:%m:%Y', time.localtime(timeStamp))
    hmsV = time.strftime('%H:%M:%S', time.localtime(timeStamp))
    hourV = time.strftime('%H', time.localtime(timeStamp))
    millsecondV = str(timeStamp).split(".")[1][:3]
    return (ymdFV, hmsV + ":" + millsecondV, hourV, ymdBV)


def createLogLine(message):
    """
    Format the CAN message
    """
    # Time Stamp
    (ymdFV, hmsfV, hourV, ymdBV) = extractTimeFromEpoch(message.timestamp)

    # PGN
    pgnV = '0x{:02x}'.format(message.arbitration_id)

    # Hex
    hexV = ''
    for i in range(message.dlc):
        hexV += '{0:x} '.format(message.data[i])

    outstr = " ".join([hmsfV, "Rx", "1", pgnV, "x", str(message.dlc), hexV]) + " "
    timeDateV = (ymdFV, hourV, ymdBV, hmsfV)
    return (outstr, timeDateV)


def can_rx_task(bus, outDir, numCAN, bRate, CANv, numTank, volumeL):
    """
    CAN receive thread
    """
    curFname = None
    outF = None
    prevTime = ("-1", "-1", "-1")

    livefeedNiraErrorFname = "_".join([outDir, CANv, "liveUpdate-NiraError.txt"])
    livefeedHmassFname = "_".join([outDir, CANv, "liveUpdate-Hmass.txt"])

    prevNiraError = None

    tempL = []
    maxNumTanks = 6
    for i in range(maxNumTanks): tempL.append(None)
    presT1 = None
    wheelSpeed = None
    railPressure = None

    prevSec = None

    curVarL = [railPressure, presT1, wheelSpeed]

    while True:
        # recieve message and extract info
        (outstr, timeDateV) = createLogLine(bus.recv())

        (ymdFV, hourV, ymdBV, hmsfV) = timeDateV

        prevYmdBV = ymdBV
        prevHmsfV = hmsfV
        prevHour = hourV
        prevTime = (prevYmdBV, prevHmsfV, prevHour)

        (prevNiraError, tempL, curVarL, prevSec) = liveUpdateTruck(outstr, livefeedNiraErrorFname,
                                                                   livefeedHmassFname,
                                                                   prevNiraError, prevTime, tempL,
                                                                   curVarL, volumeL, numTank,
                                                                   maxNumTanks, prevSec)
        # if not(HtotalMass == None):
        #     WRITE CODE HERE ... use HtotalMass


def readwriteMessageThread(bus, outDir, numCAN, bRate, CANv, numTank, volumeL):
    """
    In seperate thread continually recieve messages from CAN logger
    """
    # Start receive thread
    t = Thread(target=can_rx_task, args=(bus, outDir, numCAN, bRate, CANv, numTank, volumeL))
    t.start()





def msg_recieving():
    outDir = sys.argv[1]  # "/home/pi/rough/logger-rbp-python-out/lomack150_"
    numCAN = int(sys.argv[2])  # 2
    bRate = int(sys.argv[3])  # 250000 or 500000
    CANtype = sys.argv[4]  # OCAN or ACAN
    numTank = int(sys.argv[5])
    volumeStr = sys.argv[6]

    volumeL = [float(x) for x in volumeStr.split(",")]

    os.system("sudo /sbin/ip link set can0 down")
    if numCAN == 2:
        os.system("sudo /sbin/ip link set can1 down")

    # Make CAN interface to 250 or 500kbps
    setCANbaudRate(numCAN, bRate)

    # Connect to Bus
    bus0 = connectToLogger('can0')
    if numCAN == 2:
        bus1 = connectToLogger('can1')

    # Continually recieved messages
    readwriteMessageThread(bus0, outDir, numCAN, bRate, CANtype, numTank, volumeL)
    # if numCAN == 2:
    #    readwriteMessageThread(bus1, outDir, numCAN, bRate, CANtype + "1", numTank, volumeL)

    # Continually write readMessages
    try:
        while True:
            pass

    except KeyboardInterrupt:
        # Catch keyboard interrupt
        os.system("sudo /sbin/ip link set can0 down")
        if numCAN == 2:
            os.system("sudo /sbin/ip link set can1 down")
        print('\n\rKeyboard interrtupt')


if __name__ == "__main__":
    main()


