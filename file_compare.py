# Take 2 files and compare them -- delete from the second file any duplicate messages present in the first file

fref = open('/Users/Xavier/Desktop/Kivystuff/Truck Monitoring/Truck Screen/logs/ROUND2/default_test__4.txt', 'r')
fcomp = open('/Users/Xavier/Desktop/Kivystuff/Truck Monitoring/Truck Screen/logs/ROUND2/send_test_msg_7.txt', 'r')
funique = open('output.txt', 'w')

ref_lines = fref.readlines()
comp_lines = fcomp.readlines()

unique_messages = []

unique = True

for l in comp_lines:
    unique = True

    if l[9:15] == 'BEFORE':
        comp_start = 24
    else:
        comp_start = 23

    for line in ref_lines:

        if line[9:15] == 'BEFORE':
            ref_start = 24
        else:
            ref_start = 23

        #print(m_start)
        if l[comp_start:] == line[ref_start:]:
            unique = False

    if unique:
        unique_messages.append(l[comp_start:])

singles = []


for message in unique_messages:

    count = 0


    for item in unique_messages:

        if message == item:
            count += 1

        if count > 1:
            dupli = True
            
    funique.write(message)


fref.close()
fcomp.close()
funique.close()

print(unique_messages)