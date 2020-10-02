import serial
from time import sleep


def main():
    code_dir = 'Display_rep/'
    ser = serial.Serial('/dev/ttyS0', 9600, )

    '''ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )'''




    fin = open(code_dir + "serial_data.txt", "w")

    while True:
        recieved_data = ser.read()
        sleep(0.03)
        data_left = ser.inWaiting()
        recieved_data += ser.read(data_left)
        print(recieved_data)
        fin.write(str(recieved_data) + '\n')
        #print('Data: ' + recieved_data)



if __name__ == '__main__':
    main()
