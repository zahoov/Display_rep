#!/bin/sh

codeDir="/home/pi/"

stty -F /dev/ttyS0 raw 9600 cs8 clocal

cat /dev/ttyS0 | tr -dc '\0-\177' | python3 ${codeDir}recordGPS/extractGPS_RBP_v2.py

