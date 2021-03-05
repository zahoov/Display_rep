import os
import time


def dusk_check():

    fin = open('/Users/Xavier/Desktop/Kivystuff/Truck Monitoring/Truck Screen/sunsets.txt', 'r')

    dusk_list = fin.readlines()

    this_month = time.strftime('%m')
    real_today = time.strftime('%d')

    if int(real_today) <= 3:
        sudo_today = '01'
    elif int(real_today) <= 10:
        sudo_today = '07'
    elif int(real_today) <= 17:
        sudo_today = '14'
    elif int(real_today) <= 23:
        sudo_today = '20'
    else:
        sudo_today = '26'

    for line in dusk_list:

        dusk_month = line.split('>')[0].split('-')[0]
        dusk_day = line.split('>')[0].split('-')[1]

        if dusk_month == this_month:

            dusk_time = line.split('>')[1].strip('\n')

            if dusk_day == sudo_today:

                print(dusk_time)

    fin.close()

if __name__ == '__main__':
    dusk_check()