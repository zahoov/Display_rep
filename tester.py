
#/Users/Xavier/Desktop/Kivystuff/Truck Monitoring/Truck Screen/dataanalysis_20201009_RP18.txt

'''fin = open('Display_rep/logs/', 'r')
count = 0
i = 0
lines = fin.readlines()

for l in lines:'''
#a = b'\xce'b'\xc2'b'\x00'b'p

'''if l[22:26] == 'FECA':
    count += 1
    if l[29:33] == 'x 8 ':
        print('yes')
        i += 1'''

messages = []
message_file = open("test_messages.txt", 'r')
clean_msg = ''


for line in message_file:
    stripped_line = line.rstrip()
    messages.append(stripped_line)

msg = messages[2].split(', ')




#a = b'\xac\x00.'


'''
for item in msg:
    msg[count] = int(item, 16)
    msg[count] = hex(msg[count])
    count += 1


a = list(a)
b = []
hexlist = ['{:X}'.format(num) for num in a]

for hex in hexlist:
    b.append(int(hex, 16))

print(*hexlist)
print(*b)
'''
