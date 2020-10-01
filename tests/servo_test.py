import time, socket, smtplib, serial, threading, os

import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode (IO.BCM)

IO.setup(17,IO.OUT) #BLUE
servo1 = IO.PWM(17,50) # pin 11 for servo1, pulse 50Hz

IO.setup(21,IO.OUT) ## RED
servo2 = IO.PWM(21,50) # pin 11 for servo1, pulse 50Hz

def door_reset():
    print("closing doors")
    for i in range(1,27):
        servo1.ChangeDutyCycle(6+i/5)
        servo2.ChangeDutyCycle(12-i/5)
        time.sleep(0.02)
    #servo1.ChangeDutyCycle(12)
    #servo2.ChangeDutyCycle(6)
    #time.sleep(.3)
    servo1.ChangeDutyCycle(6)
    servo2.ChangeDutyCycle(12)
    time.sleep(.3)
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

servo1.start(0)
servo2.start(0)

while True:
    door_reset()
    time.sleep(3)

servo1.ChangeDutyCycle(0)
servo2.ChangeDutyCycle(0)
