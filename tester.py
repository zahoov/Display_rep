
import time

code_dir = '/Users/Xavier Biancardi/PycharmProjects/Display_rep/'
bRate = 9600


x = b'\x80T\x00\xbe\x00\x00U\x00[\x00F\x80\xf8'

x = list(x)

hexlist = ['{:X}'.format(num) for num in x]
print(*hexlist)