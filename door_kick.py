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
    for i in range(1,30):
        servo1.ChangeDutyCycle(6+i/5)
        servo2.ChangeDutyCycle(12-i/5)
        time.sleep(0.02)

    servo1.ChangeDutyCycle(6)
    servo2.ChangeDutyCycle(12)
    time.sleep(.3)
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)
    
def door_kick():
    print("pushing doors left")
    servo1.ChangeDutyCycle(6)
    time.sleep(0.3)
    servo1.ChangeDutyCycle(12.5)
    time.sleep(0.3)
    servo1.ChangeDutyCycle(6)
    time.sleep(0.3)
    servo1.ChangeDutyCycle(0)
    
    time.sleep(.5)
    
    print("pushing doors right")
    servo2.ChangeDutyCycle(12)
    time.sleep(0.3)
    servo2.ChangeDutyCycle(5.5)
    time.sleep(0.3)
    servo2.ChangeDutyCycle(12)
    time.sleep(0.3)
    servo2.ChangeDutyCycle(0)
    
    time.sleep(.5)

servo1.start(0)
servo2.start(0)

for x in range(3):
    door_kick()
    time.sleep(3)
door_reset()

