#!/bin/sh

numCAN=1
bRate=250000
CANtype="RBP19"
truckName="bigWhite"

numTank=5
volumeStr="202,202,202,202,148"

codeDir="/home/pi/recordCAN/"
outDir="/home/pi/outCAN/${truckName}"

mkdir -p /home/pi/outCAN/

sudo python3 ${codeDir}recordCANlogger.py ${outDir} ${numCAN} ${bRate} ${CANtype} ${numTank} ${volumeStr}

