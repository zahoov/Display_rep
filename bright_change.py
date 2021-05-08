import os
import time
import requests

fin = open('/Users/Xavier Biancardi/PycharmProjects/Display_rep/2021PrinceGeorgeSunsets.txt', 'w')

i = 1


while i <= 12:

    d = [1, 7, 14, 20, 26]

    for day in d:

        cur_date = '2021-' + str(i) + '-' + str(day)
        if i >= 10:

            cur_date_str = '2021-' + str(i) + '-' + str(day)

        else:
            cur_date_str = '2021-' + '0' + str(i) + '-' + str(day)

        url = 'https://api.sunrise-sunset.org/json?lat=53.9195387498915&lng=-122.7517381789694&date=' + cur_date

        receive = requests.get(url)

        #print(receive.text)



        a = receive.text.split(',')

        utc_hour = a[1].split('"')[3].split(':')[0]
        min = a[1].split('"')[3].split(':')[1]




        #if i == 5:
            #print(receive.text)

            #print(utc_hour)

        pst_hour = int(utc_hour) + 4
        #print(min)

        if pst_hour > 12:
            pst_hour = pst_hour - 12
            #pst = str(pst_hour) + min


        pst = '0' + str(pst_hour) + ':' + min

        fin.write(cur_date_str + '>' + pst + '\n')

    i += 1

fin.close()

