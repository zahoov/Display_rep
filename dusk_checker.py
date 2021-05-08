import os
import time


def dusk_check():

    fin = open('/Users/Xavier Biancardi/PycharmProjects/Display_rep/2021PrinceGeorgeSunsets.txt', 'r')

    dusk_list = fin.readlines()

    this_month = time.strftime('%m')
    real_today = time.strftime('%d')

    if int(real_today) <= 3:
        sudo_today = '1'
    elif int(real_today) <= 10:
        sudo_today = '7'
    elif int(real_today) <= 17:
        sudo_today = '14'
    elif int(real_today) <= 23:
        sudo_today = '20'
    else:
        sudo_today = '26'


    for line in dusk_list:

        dusk_month = line.split('>')[0].split('-')[1]
        dusk_day = line.split('>')[0].split('-')[2]


        if dusk_month == this_month:

            dusk_time = line.split('>')[1].strip('\n')



            if dusk_day == sudo_today:

                if (int(this_month) > 3) or (int(this_month) < 11):
                    DST = True

                elif (int(this_month == 3)) and (int(real_today) >= 14):
                    DST = True

                elif(int(this_month == 11)) and (int(real_today) < 7):
                    DST = True
                else:
                    DST = False

                if DST == True:
                    dhour = int(dusk_time.split(':')[0]) + 1
                    dmin = int(dusk_time.split(':')[1])
                    dusk_time = str(dhour) + ':' + str(dmin)


                    
                print(dusk_time)

    fin.close()

if __name__ == '__main__':
    dusk_check()