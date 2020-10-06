
import time

code_dir = '/Users/Xavier Biancardi/PycharmProjects/Display_rep/'
bRate = 9600

def topOfFile(ymdBV, hmsfV, bRate):
    """
    Top of log file message
    """
    loggerVersion = "1.1.1"
    topLineL = ["***RPIMASTER Ver " + loggerVersion + "***",
                "***PROTOCOL CAN***",
                "***NOTE: PLEASE DO NOT EDIT THIS DOCUMENT***",
                "***[START LOGGING SESSION]***",
                "***START DATE AND TIME " + ymdBV + " " + hmsfV + "***",
                "***HEX***",
                "***SYSTEM MODE***",
                "***START CHANNEL BAUD RATE***",
                "***CHANNEL TTYS0" + str(
                    bRate) + " bps***",
                "***END CHANNEL BAUD RATE***",
                "***START DATABASE FILES***",
                "***END DATABASE FILES***",
                "***<Time><Tx/Rx><Channel><CAN ID><Type><DLC><DataBytes>***"]
    return "\n".join(topLineL) + "\n"

def bottomOfFile(prevYmdBV, prevHmsfV):
    """
    Bottom of the file
    """
    bottomLineL = ["***END DATE AND TIME " + prevYmdBV + " " + prevHmsfV + "***",
                   "***[STOP LOGGING SESSION]***"]
    return "\n".join(bottomLineL) + "\n"







if __name__ == '__main__':
    file_setup()
