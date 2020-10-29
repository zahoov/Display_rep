
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
'''
#b'\x80'b'\xf7'b'\x04'b'"'b'\xcc'b'\x02'b'\x00'b'\x95'
a = b'\x80'b'd'b'\x00'b'n'b'@'b'\xaf'b'\xfa'b'\x00'b'Y'b'\x00'b'\xa8'b'\x02'b'\x01'b'\xad'b'\x13'b'\x01'b'f'b'\x00'b'\x9a'


a = list(a)
b = []
hexlist = ['{:X}'.format(num) for num in a]

for hex in hexlist:
    b.append(int(hex, 16))

print(*hexlist)
print(*b)
'''

msg = [0x40, 0x00, 0x84]

message = bytes(msg)

mid = message[0].to_bytes(1, 'big')

print(mid)


