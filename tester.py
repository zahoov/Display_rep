
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
#a = b'\x00'b'['b'\x00'


'''a = list(a)
b = []
hexlist = ['{:X}'.format(num) for num in a]

for hex in hexlist:
    b.append(int(hex, 16))

print(*hexlist)
print(*b)'''


fin = open('test_files/hydraFL_20200917runMILError_RBP18_H_bus.log', 'r')
fref = open('dm_hex.txt', 'r')

lines = fin.readlines()
dm_messages = []

present_dm = []
i = 0

for line in fref:
    dm_messages.append(line.rstrip())

for l in lines:

    for dm in dm_messages:
        #print(dm)

        if l[22:26] == dm:

            duplicate = False

            for item in present_dm:
                if item == dm:
                    duplicate = True

            if not duplicate:
                present_dm.append(dm)

print(present_dm)












