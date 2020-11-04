fin = open('hydraFL_20200917runMILError_RBP18_H_bus.log', 'r')
count = 0
i = 0
lines = fin.readlines()
lines_list = []

for l in lines:
    i += 1
    if i >= 13:

        if l[22:26] == 'FECA':
            #count += 1


            first_byte = (str(bin(int(l[55:57], 16))))[2:4]

            if first_byte == '0':
                #o_count = str(bin(int(l[48:50], 16)))
                o_count = l[40:42]
                lines_list.append(i)
                print(o_count)




print(lines_list)