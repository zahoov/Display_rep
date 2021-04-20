import subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# wait for the pin to be sorted with GND and, if so, halt the system
GPIO.wait_for_edge(25, GPIO.FALLING)
subprocess.call(['shutdown -h -P now "System halted by GPIO action"'], shell=True)

# clean up GPIO on normal exit
GPIO.cleanup()