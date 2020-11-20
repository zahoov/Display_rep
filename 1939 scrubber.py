fin = open('test_files/hydraFL_20200925test_RBP18_H_bus.log', 'r')
dms = open('dm_list.txt', 'r')
count = 0
i = 0
lines = fin.readlines()
lines_list = []
message_list = []
c = 1
wow = False

for l in lines:
    i += 1
    if i >= 13:

        if l[22:28] == 'FECA01':



            first_byte = (format(int(l[33:35], 16), '08b'))[:2]
            full_byte = (format(int(l[33:35], 16), '08b'))
            o_count = int(l[48:50], 16)

            count += 1



            '''if (o_count == 3):# and (first_byte == '00'):
                print(l)
                exit()
                count += 1
                #print(o_count)
                wow = l
                message_list.append(l)
                lines_list.append(i)
                #count += 1'''


            #print(first_byte)

            '''if c == 1:
                if o_count == 2:
                    c += 1
                    print('nice')
                    print(i)
                    print(l)'''


            '''
            
                print(first_byte)
                count += 1
                lines_list.append(i)
                message_list.append(l)
            '''

print(count)
#a = len(message_list)
#print(wow)
#print(message_list)