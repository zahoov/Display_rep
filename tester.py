import serial


def main():
    code_dir = 'Display_rep/'
    ser = serial.Serial('/dev/ttyS0')
    fin = open(code_dir + "fuel_file.txt", "w")

    while True:

        print('its in the loop now')

        try:
            print('its the try')
            recieved_data = ser.readline()
            fin.write(str(recieved_data))
            print('Data: ' + recieved_data)

        except KeyboardInterrupt:
            fin.close()
            print('this should stop it?')
            return


if __name__ == '__main__':
    main()


