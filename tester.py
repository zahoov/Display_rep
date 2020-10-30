
#/Users/Xavier/Desktop/Kivystuff/Truck Monitoring/Truck Screen/dataanalysis_20201009_RP18.txt

'''fin = open('Display_rep/logs/', 'r')
count = 0
i = 0
lines = fin.readlines()

for l in lines:'''


'''if l[22:26] == 'FECA':
    count += 1
    if l[29:33] == 'x 8 ':
        print('yes')
        i += 1'''

#b'\x80'b'\xfa'b'\x04'b'o'b'\x19'b'\x06'b'\x00'b'\xf4'
a = b'\x80'b'V'b'\x00'b'b'b'\x00'b'\xf5'b'\x04'b'q'b'\x95'b'3'b'\x00'b'\x96'


a = list(a)
b = []
hexlist = ['{:X}'.format(num) for num in a]

for hex in hexlist:
    b.append(int(hex, 16))

print(*hexlist)
print(*b)




