import serial
import time
import random
import struct
from functools import reduce
from multiprocessing import Process, Pipe, Lock

TENBITTIMES = 104.16 * 10 / (10 ** 6)
ONEBITTIME = 104.16 / (10 ** 6)


def message_constructor(msg):
    thismsg = bytes(msg)
    chksum = struct.pack('b', checksum(thismsg))
    thismsg += chksum

    return thismsg

def checksum(msg):
    return toSignedChar(~reduce(lambda x, y: (x + y) & 0xFF, list(msg)) + 1)

def toSignedChar(num):
    if type(num) is bytes:
        return struct.unpack('b', num)[0]
    else:
        return struct.unpack('b', struct.pack('B', num & 0xFF))[0]

def check(msg):
    if type(msg[0]) is bytes:
        thismsg = list(map(lambda x: int.from_bytes(x, byteorder='big'), msg))
    else:
        thismsg = msg
    return toSignedChar(reduce(lambda x, y: (x + y) & 0xFF, list(thismsg)))

def getmsg(busport):
    finished = False
    msg = []

    ttimeout = busport.timeout
    busport.timeout = TENBITTIMES
    tempb = b''
    # periodically timeout and let a blocking sender go.
    while tempb is b'':
        tempb = busport.read(1)
        #if tempb is b'':
            #pass
            #buslock.release()
            #buslock.acquire()
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

    busport.timeout = ttimeout
    #buslock.release()
    #if len(msg) <= 1 or not check(msg[:-1]) + toSignedChar(msg[-1]) == 0:
        #		initialize(busport,buslock)
     #   return None

    return msg[0]

def initialize(busport):
    idle = False
    # buslock.acquire()
    init_start_time = time.time()
    #busport.flushInput()
    #busport.timeout = 0
    while not idle:
        # print(time.clock())
        a = busport.read(1)
        if not a is b'':
            init_start_time = time.time()
        elif time.time() - init_start_time < TENBITTIMES:
            continue
        else:
            idle = True

    # buslock.release()

def priority_delay(priority):
    p_delay = ONEBITTIME * 2 * priority

    return p_delay


def init_double_check(busport):
    # buslock.aquire()

    a = busport.read(1)
    if a is b'':
        idle = True
    else:
        idle = False
        initialize(busport)

    # buslock.release()
    return idle


#def mid_transmit(busport, mid):
    # buslock.aquire()

    # buslock.release()


def mid_receive(busport, mid):
    # buslock.aquire()
    busport.write(mid)

    mid_read = busport.read(1)
    print(mid_read)
    if mid_read is mid:
        bus_claim = True
    else:
        bus_claim = False


    # buslock.release()
    return bus_claim, mid_read




def packet_sender(busport, bus_claim, message):
    if bus_claim:
        # buslock.aquire()
        busport.write(message)
        # buslock.release()


# 10 Wait  for  a  pseudo-random  number  of  bit  times(between 0-7)

def pseudo_random():
    pseudo_delay = random.randint(0, 7)
    return pseudo_delay


# 11 Go to step 3

if __name__ == '__main__':

    path = 'Display_rep/logs/' + 'ROUND3'

    com = serial.Serial()
    com.port = "/dev/ttyS0"
    com.baudrate = 9600
    com.timeout = (1 / 9600) * 22
    #com.STOPBITS = 1
    #com.PARITIES = 0
    com.set_buffer_size = 21
    #com.interCharTimeout = 0.01

    # buslock = Lock()

    testing = True

    messages = []
    message_file = open("Display_rep/test_messages.txt", 'r')

    is_first_collision = True

    if ~com.is_open:
        com.open()

    for line in message_file:
        stripped_line = line.rstrip()
        messages.append(stripped_line)

    index = 0

    msg = [0x40, 0x00, 0x84]
    message_2 = [0xb4, 0xc3, 0x03, 0x80, 0x97, 0x3e]
    message_3 = [0xac, 0x00, 0x2e]

    fin = open('Display_rep/logs/MATCO_Tests/' + time.strftime("%d_%H_%M") + '.txt', 'w')

    step = 1

    while testing is True:

        # Step 1 Check if idle
        # The bus is Idle after 10-bit times have elapsed from the previous character with no received Start bits.
        if step == 1:

            initialize(com)  # step 1
            step += 1

        # Step 2 wait the required priority delay after the idle period has begun --> Pd = Tb*2*P,
        # where: Pd = priority delay, Tb = Bit time (104.16 us), P = priority
        elif step == 2:

            prio_delay = priority_delay(priority=8)  # step 2
            time.sleep(prio_delay)  # step 2
            step += 1

        # Step 3 make sure the bus is still idle, if it is not idle go back to step 1
        elif step == 3:

            idle = init_double_check(com)  # step 3
            if not idle:
                step = 1
            else:
                step += 2

        # Step 4 transmit the device MID on the bus
        #elif step == 4:
            #print(msg[0])

            #mid_transmit(com, msg[0])
            #step += 1

        # Step 5 Receive the transmitted MID and determine that the sent MID matches the received MID
        elif step == 5:

            #bus_claim, mid_read = mid_receive(com, msg[0])
            bus_claim = False
            com.write(msg[0])
            print(msg[0])
            mid = getmsg(com)


            print(mid)

            if mid == msg[0]:
                bus_claim = True
            else:
                bus_claim = False


            fin.write(str(mid))

            # Step 7 If  the  match  failed,  we  lost  the  arbitration.Continue to step 8
            if not bus_claim:

                # Step 8 If this was the first collision for this packet, go to step 1
                if is_first_collision:
                    step = 1
                    is_first_collision = False

                else:
                    # step 9
                    idle = initialize(com)
                    step += 1

            # Step 6 If  the  match  was  successful,  we  have  claimed the bus. Send the packet
            elif bus_claim:
                packet_sender(com, bus_claim, msg)
                step = 7

        elif step == 6:
            rand_num_bit_times = pseudo_random()
            delay_duration = rand_num_bit_times * ONEBITTIME
            time.sleep(delay_duration)

            step = 3

        elif step == 7:
            is_first_collision = True
            testing = False

            x = 0
            while x < 30:
                a = getmsg(com)

                if a is not None:
                    print(a)
                    a = list(a)
                    # hexlist = ['{:X}'.format(num) for num in a]
                    out = ''
                    for num in a:
                        out += str(num)

                    outstr = " ".join([time.strftime("%H:%M:%S"), 'AFTER REQUEST', out, '\n'])
                    fin.write(outstr)
                    x += 1
            fin.close()



        print(step)


