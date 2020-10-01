import serial


def main():
    code_dir = 'Display_rep/'
    ser = serial.Serial('/dev/ttyS0', 9600)
    fin = open(code_dir + "serial_data.txt", "w")

    while True:

        print('its in the loop now')

        try:
            print('its the try')
            recieved_data = ser.readline()
            print('its past the readline')
            fin.write(str(recieved_data))
            print('Data: ' + recieved_data)

        except KeyboardInterrupt:
            fin.close()
            print('this should stop it?')
            return


if __name__ == '__main__':
    main()


