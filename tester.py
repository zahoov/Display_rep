import serial
import os
from time import sleep


def main():
    code_dir = 'Display_rep/'
    ser = serial.Serial('/dev/')
    fin = open(code_dir + "fuel_file.txt", "w")

    while True:

        try:
            recieved_data = ser.readline()
            fin.write(str(recieved_data))

        except KeyboardInterrupt:
            fin.close()
            pass


if __name__ == '__main__':
    main()