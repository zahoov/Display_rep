import can
import os
import time
from datetime import datetime

experimental_timestamps = []
time_deltas = []

FMT = "%H:%M:%S:%f"
micro_in_sec = 1000000

prev_timestamp = None

filename = None

while filename == None:
    try:
        filename = input('Enter the file name to read:\n')
        fin = open(filename, 'r')
    except(FileNotFoundError):
        print("That file doesn't exist")
        filename = None

lines = fin.readlines()
i = 0
fin.close()

bRate = input("Choose the baudrate for data transmission\n1:250000\n2:500000\n")
bRate = '1'
if bRate == '1':
    bRate = 250000
else:
    bRate = 500000

os.system("sudo /sbin/ip link set can0 up type can bitrate " + str(bRate))
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')


for l in lines:

    if l[0] == '*':
        pass
    else:

        line = l.split(' ')
        cur_timestamp = line[0]
        #print(line[6:14])
        can_data = []

        for item in line[6:14]:
            can_data.append((int(item, 16)))

        #can_msg_data = ','.join(can_data)
        if prev_timestamp == None:
            prev_timestamp = cur_timestamp

        tdelta = (datetime.strptime(cur_timestamp, FMT) - datetime.strptime(prev_timestamp, FMT))

        tdelta_sec = tdelta.microseconds/micro_in_sec
        time_deltas.append(tdelta_sec)

        #before = (time.monotonic_ns()) / micro_in_sec
        
        msg = can.Message(data=can_data)
        bus.send(msg)
        
        prev_timestamp = cur_timestamp

        time.sleep(tdelta_sec)
        #after = (time.monotonic_ns()) / micro_in_sec

        #experimental_timestamps.append((after - before)/1000)




