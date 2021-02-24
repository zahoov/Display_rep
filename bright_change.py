import os
import time


brightness = 1024

while brightness > 0:
    dimmer = "gpio -g pwm 12 " + str(brightness)

    os.system(dimmer)

    brightness -= 16

    time.sleep(0.5)

while brightness < 1024:

    brighter = "gpio -g pwm 12 " + str(brightness)

    os.system(brighter)

    brightness += 16

    time.sleep(0.5)


