import serial
from time import sleep


def main():
    code_dir = 'Display_rep/'
    ser = serial.Serial('/dev/ttyS0', 9600)
    fin = open(code_dir + "serial_data.txt", "w")

    while True:
        recieved_data = ser.read()
        sleep(0.03)
        data_left = ser.inWaiting()
        recieved_data += ser.read(data_left)
        print(recieved_data)
        fin.write(str(recieved_data))
        #print('Data: ' + recieved_data)



if __name__ == '__main__':
    main()
