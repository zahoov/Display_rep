import serial
from time import sleep


def main():
    code_dir = 'Display_rep/'
    ser = serial.Serial('/dev/ttyS0')
    fin = open(code_dir + "fuel_file.txt", "w")
    x = 1

    while x == 1:

        try:
            recieved_data = ser.readline()
            fin.write(str(recieved_data))
            print(recieved_data)

        except KeyboardInterrupt:
            fin.close()
            print('this should stop it?')
            return


if __name__ == '__main__':
    main()