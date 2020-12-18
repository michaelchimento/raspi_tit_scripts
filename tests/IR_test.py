import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode (IO.BCM)
if "P3" in name:
    left_IR_pin=19
    print("changing left_push pin to {}".format(left_IR_pin)
else:
    left_IR_pin=23

if "P8" in name:
    right_IR_pin=19
    print("changing right_push pin to {}".format(right_IR_pin)

else:
    right_IR_pin=24


while 1:

    if(IO.input(left_IR_pin)==True):
        print("solve left")
    
    if(IO.input(right_IR_pin)==True):
        print("solve right")
