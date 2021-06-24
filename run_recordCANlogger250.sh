#!/bin/sh

numCAN=1
bRate=250000
CANtype="RBP19"
truckName="bigWhite"

numTank=5
volumeStr="202,202,202,202,148"

codeDir="/home/pi/Display_rep/"
outDir="/home/pi/outCAN/${truckName}"

mkdir -p /home/pi/outCAN/

sudo python3 ${codeDir}recordCANlogger250.py ${outDir} ${numCAN} ${bRate} ${CANtype} ${numTank} ${volumeStr}

