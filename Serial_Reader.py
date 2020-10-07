import serial
import datetime
from time import sleep


def main():
    bRate = 9600
    code_dir = 'Display_rep/'
    #ser = serial.Serial('/dev/ttyS0', 9600, )

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
                "***<Time><Tx/Rx><Port><MID+PID/DataBytes>***"]

    top = "\n".join(topLineL) + "\n"
    fin.writelines(top)
    i = 0

    while True:
        try:
            i = i + 1
            recieved_data = ser.read()
            
            data_left = ser.inWaiting()
            recieved_data += ser.read(data_left)

            x = list(recieved_data)
            #x = b'\x80T\x00\xbe\x00\x00U\x00[\x00F\x80\xf8'

            hexlist = ['{:X}'.format(num) for num in x]
            print(*hexlist)

            now = datetime.datetime.now()

            outstr = " ".join([now.strftime("%H:%M:%S"), "Rx", 'ttyS0', *hexlist]) + "\n"

            fin.writelines(outstr)

            if i == 50:
                return

            sleep(0.03)
        except KeyboardInterrupt:
            now = datetime.datetime.now()

            bottomLineL = ["***END DATE AND TIME " + now.strftime("%d:%m:%Y %H:%M:%S") + "***",
                           "***[STOP LOGGING SESSION]***"]
            bot = "\n".join(bottomLineL) + "\n"
            fin.writelines(bot)
            fin.close()

            return


if __name__ == '__main__':
    main()
