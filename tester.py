
import datetime

now = datetime.datetime.now()

first = now.strftime("%H")
second = int(now.strftime("%H")) + 1
third = str(second)



print(third)