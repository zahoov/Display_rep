import serial
import datetime
from time import sleep


def main():
    bRate = 9600
    code_dir = '/Users/Xavier Biancardi/PycharmProjects/Display_rep/'
    # ser = serial.Serial('/dev/ttyS0', 9600, )

    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=bRate,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    now = datetime.datetime.now()

    fin = open(code_dir + 'serial_log_' + now.strftime("%d-%m-%Y_%H-%M-%S") + ".txt", "w")

    topLineL = ["***RPIMASTER Ver " + "1.1.1" + "***",
                "***PROTOCOL CAN***",
                "***NOTE: PLEASE DO NOT EDIT THIS DOCUMENT***",
                "***[START LOGGING SESSION]***",
                "***START DATE AND TIME " + now.strftime("%d:%m:%Y %H:%M:%S") + "***",
                "***HEX***",
                "***SYSTEM MODE***",
                "***START CHANNEL BAUD RATE***",
                "***CHANNEL TTYS0" + str(
                    bRate) + " bps***",
                "***END CHANNEL BAUD RATE***",
                "***START DATABASE FILES***",
                "***END DATABASE FILES***",
                "***<Time><Tx/Rx><Channel><CAN ID><Type><DLC><DataBytes>***"]

    bottomLineL = ["***END DATE AND TIME " + now.strftime("%d:%m:%Y %H:%M:%S") + "***",
                   "***[STOP LOGGING SESSION]***"]

    fin.writelines(topLineL + '\n')

    while True:

        try:
            recieved_data = ser.read()
            sleep(0.03)
            data_left = ser.inWaiting()
            recieved_data += ser.read(data_left)
            print(recieved_data)
            fin.writelines(str(recieved_data) + '\n')

        except KeyboardInterrupt:
            fin.writelines(bottomLineL)
            fin.close()


if __name__ == '__main__':
    main()
