import serial
import datetime
from time import sleep


def main():
    bRate = 9600
    code_dir = 'Display_rep/'
    start_time = datetime.datetime.now()

    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=bRate,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    fin = open(code_dir + 'serial_log_' + start_time.strftime("%d-%m-%Y_%H-%M-%S") + ".txt", "w")

    topLineL = ["***RPIMASTER Ver " + "1.1.1" + "***",
                "***PROTOCOL CAN***",
                "***NOTE: PLEASE DO NOT EDIT THIS DOCUMENT***",
                "***[START LOGGING SESSION]***",
                "***START DATE AND TIME " + start_time.strftime("%d:%m:%Y %H:%M:%S") + "***",
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

    while True:

        now = datetime.datetime.now()

        if now.strftime("%H") == str(int(start_time.strftime("%H")) + 1):

            end_time = now
            start_time = now

            bottomLineL = ["***END DATE AND TIME " + end_time.strftime("%d:%m:%Y %H:%M:%S") + "***",
                           "***[STOP LOGGING SESSION]***"]
            bot = "\n".join(bottomLineL) + "\n"
            fin.writelines(bot)
            fin.close()

            fin = open(code_dir + 'serial_log_' + start_time.strftime("%d-%m-%Y_%H-%M-%S") + ".txt", "w")

            topLineL = ["***RPIMASTER Ver " + "1.1.1" + "***",
                        "***PROTOCOL CAN***",
                        "***NOTE: PLEASE DO NOT EDIT THIS DOCUMENT***",
                        "***[START LOGGING SESSION]***",
                        "***START DATE AND TIME " + start_time.strftime("%d:%m:%Y %H:%M:%S") + "***",
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

        else:

            try:

                recieved_data = ser.read()

                data_left = ser.inWaiting()
                recieved_data += ser.read(data_left)

                x = list(recieved_data)
                # x = b'\x80T\x00\xbe\x00\x00U\x00[\x00F\x80\xf8'

                hexlist = ['{:X}'.format(num) for num in x]
                message = str(*hexlist)

                prev_time = datetime.datetime.now()

                outstr = " ".join([prev_time.strftime("%H:%M:%S"), "Rx", 'ttyS0', message]) + "\n"

                fin.writelines(outstr)

                sleep(0.03)
            except KeyboardInterrupt:
                end_time = datetime.datetime.now()

                bottomLineL = ["***END DATE AND TIME " + end_time.strftime("%d:%m:%Y %H:%M:%S") + "***",
                               "***[STOP LOGGING SESSION]***"]
                bot = "\n".join(bottomLineL) + "\n"
                fin.writelines(bot)
                fin.close()

                return


if __name__ == '__main__':
    main()
