import serial
from multiprocessing import Process, Pipe, Lock
import time

TENBITTIMES = 0.0010416


def receiver(busport):
    while True:
        finished = False
        msg = []
        # buslock.acquire()
        ttimeout = busport.timeout
        # busport.timeout = TENBITTIMES
        tempb = b''
        # periodically timeout and let a blocking sender go.
        while tempb is b'':
            tempb = busport.read(1)
            # if tempb is b'':
            #    buslock.release()
            #    buslock.acquire()
        msg += [tempb]
        busport.timeout = 0
        stime = time.time()

        while not finished:
            a = busport.read(1)
            t = time.time()
            if a is b'' and t - stime > TENBITTIMES:
                finished = True
            elif a is b'':
                continue
            else:
                stime = t
                msg += [a]

        out = []
        for num in msg:
            out += str(num)

        outstr = " ".join([time.strftime("%D:%H:%M:%S"), out, '\n'])

        fin.write(outstr)


def sender(busport, msg):

    start = int(time.strftime("%M%S"))

    while True:

        now = int(time.strftime("%M%S"))

        if now - start > 10:
            busport.write(msg)
            start = int(time.strftime("%M%S"))


fin = open('constant_read_w_send.txt', 'w')

ser = serial.Serial('/dev/ttyS0', 9600)

msg = [0x40, 0x00, 0x84, 0x3c]

rec = Process(target=receiver(ser))
send = Process(target=sender(ser, msg[0]))

rec.start()
send.start()
