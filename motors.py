from lx16a import *
from time import sleep

# If doesn't work, try each port in /dev/
LX16A.initialize('/dev/ttyUSB0')
servo1 = LX16A(1)

servo1.motor_mode(500)
sleep(100)
servo1.motor_mode(0)