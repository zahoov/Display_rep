
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

a = b'\xce'b'\xc2'b'\x00'b'p'
count = 0
messages = []
message_file = open("test_messages.txt", 'r')


for line in message_file:
    stripped_line = line.rstrip()
    messages.append(stripped_line)

for thing in messages:

    msg = messages[count].split(', ')
    count += 1
    #fin = open('logs/send_test_msg_' + str(count) + '.txt', 'w')
    i = 0
    # if mode == 1:

print(msg)
print(type(msg[3]))




