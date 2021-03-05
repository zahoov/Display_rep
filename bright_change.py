import os
import time
import requests

#fin = open('/Users/Xavier/Desktop/Kivystuff/Truck Monitoring/Truck Screen/sunsets.txt', 'w')

i = 1


while i <= 12:

    d = [1, 7, 14, 20, 26]

    for day in d:

        cur_date = '2021-' + str(i) + '-' + str(day)

        url = 'https://api.sunrise-sunset.org/json?lat=49.169611&lng=-122.946766&date=' + cur_date

        #receive = requests.get(url)

        print(receive.text)

        a = receive.text.split(',')

        utc_hour = a[5].split('"')[3].split(':')[0]
        min = a[5].split('"')[3][2:4]

        pst_hour = int(utc_hour) + 4

        if pst_hour > 12:
            print('wow')

        pst = str(pst_hour) + ':' + min

        fin.write(cur_date + '>' + pst + '\n')

    i += 1

fin.close()

