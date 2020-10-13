


fin = open('/Users/Xavier/Desktop/Kivystuff/Truck Monitoring/Truck Screen/dataanalysis_20201009_RP18.txt', 'r')
count = 0
i = 0
lines = fin.readlines()

for l in lines:
    if l[22:26] == 'FECA':
        count += 1
        if l[29:33] == 'x 8 ':
            print('yes')
            i += 1
print(i)
print(count)







