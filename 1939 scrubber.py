
#dms = open('dm_list.txt', 'r')
count = 0

i = 0

lines_list = []
message_list = []
c = 1
wow = False

log_list = ['3', '4', '11', '24', '25']

fin = open('attachments/Dec2_dm3.log', 'r')
lines = fin.readlines()

for l in lines:
    i += 1

    if i >= 13:

        #print(l[23:27])

        if l[23:27] == 'F005':

            count += 1

            first_2_bits = (format(int(l[33:35], 16), '08b'))[:2]
            full_byte = (format(int(l[33:35], 16), '08b'))
            o_count = int(l[48:50], 16)






fin.close()

print(count)

