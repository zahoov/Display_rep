#!/usr/bin/env python

import sys
import os

###################################################################################################
###################################################################################################
###################################################################################################

# Changeable variables

_outDir = "/home/pi/outGPS/"
_truckname = "bigWhite"

# Hard coded variables

_RBPid = "RBP19"
_codeDir = "/home/pi/recordGPS/" 

sys.path.insert(0, _codeDir)
from NMEAParser import NMEAParser

###################################################################################################
###################################################################################################
###################################################################################################

def makeSeriesList(colNames, parser):
    seriesValues = []

    if parser.attributeMap["latitudeDirection"] == "S":
        parser.attributeMap["latitude"] = -(parser.attributeMap["latitude"])

    if parser.attributeMap["longitudeDirection"] == "W":
        parser.attributeMap["longitude"] = -(parser.attributeMap["longitude"])

    for colName in colNames:
        seriesValues.append(parser.attributeMap[colName])

    return seriesValues

def writeToFileGPS(prevGGAL, prevRMCL, prevTime, prevYMD, GPSColNames):
    
    prevH = prevTime.split(":")[0]
    prevH = ((2 - len(prevH)) * "0") + prevH

    prevYMDformat2 = "".join(prevYMD.split("-"))
    
    newLineL = prevGGAL + prevRMCL
    
    newLine = "\t".join([prevYMD, prevTime + ":000"] + [str(value) for value in newLineL])
    
    curFname = _outDir + _truckname + "_" + prevYMDformat2 + prevH + "_GPS_" + _RBPid
    
    if os.path.isfile(curFname + ".txt"):
        outF = open(curFname + ".txt", "a")
    else:
        outF = open(curFname + ".txt", "w")
        outF.writelines("\t".join(["#Date", "Time"] + GPSColNames[1:-1]) + "\n")
    
    outF.writelines(newLine + "\n")

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def main():

    # Column names
    GPSColNames = ["timestamp", "latitude",
                   "longitude", "GPSQuality",
                   "numSatellites", "horizontalDilution",
                   "geoidHeight", "geoidUnits",
                   "status", "knotSpeed",
                   "trackAngle", "date"]

    prevTime = None
    prevGGAL= [""] * 7
    prevRMCL = [""] * 3
    prevYMD = None

    # filters gps data from stdin pipe and assigns them to dataframe
    for line in sys.stdin:
        try:
            line = line.rstrip().replace('\r','')

            typeV = line.split(",")[0]
            if typeV == "$GPGGA":
            
                curGGA = NMEAParser(line)
            
                curTime = str(curGGA.attributeMap["timestamp"])
                if not(curGGA.incomplete):
                    if (prevYMD != None) and (prevTime != None) and (curTime != prevTime):
                        if (prevGGAL != [""] * 3) and (prevRMCL != [""] * 3):
                            writeToFileGPS(prevGGAL, prevRMCL, prevTime, prevYMD, GPSColNames)
                            prevRMCL = [""] * 3
                            prevYMD = None

                    curGGAL = makeSeriesList(GPSColNames[1:8], curGGA)
                    prevTime = curTime
                    prevGGAL = curGGAL

            elif typeV == "$GPRMC":
            
                curRMC = NMEAParser(line)
            
                curTime = str(curRMC.attributeMap["timestamp"])
                curYMD = str(curRMC.attributeMap["date"])
                
                if not(curRMC.incomplete):
                    if (prevYMD != None) and (prevTime != None) and (curTime != prevTime):
                        if (prevGGAL != [""] * 3) and (prevRMCL != [""] * 3):
                            writeToFileGPS(prevGGAL, prevRMCL, prevTime, prevYMD, GPSColNames)
                            prevGGAL = [""] * 7
                
                    curRMCL = makeSeriesList(GPSColNames[-4:-1], curRMC)
                    prevTime = curTime
                    prevRMCL = curRMCL
                    prevYMD = curYMD

        except AttributeError:
            pass
        except UnicodeDecodeError:
            print("UnicodeDecodeError")

if __name__ == "__main__":
    main()

