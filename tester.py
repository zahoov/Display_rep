

'''x = b'\x80T\x00\xbe\x00\x00U\x00[\x00F\x80\xf8'
intlist = []
hexlist = ['{:X}'.format(num) for num in x]
print(*hexlist)

for hex in hexlist:
    intlist.append(int(hex, 16))

print(intlist)'''


b = [b'\x80', b'\xab', b'\x00', b'\x80', b'U']
int_list = []
hex_list = []

for num in b:
    int_list.append(int.from_bytes(num, 'big'))

for num in int_list:
    hex_list.append(str(hex(num))[2:])



print(*int_list)

#hexlist = ['{:X}'.format(num) for num in x]










