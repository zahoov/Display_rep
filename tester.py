
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

a = b'B'b'\x00'b'\xc2'b'\xfc'
messages = []
message_file = open("test_messages.txt", 'r')

hexlist = ['{:X}'.format(num) for num in a]
for item in hexlist:
    messages.append(int(item, 16))
print(hexlist)
print(messages)
#for line in message_file:
#    stripped_line = line.rstrip()
#    messages.append(stripped_line)

#for thing in messages:

#    msg = messages[count].split(', ')
#    count += 1
    #fin = open('logs/send_test_msg_' + str(count) + '.txt', 'w')
  #  i = 0
    # if mode == 1:






