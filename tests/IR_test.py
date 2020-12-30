import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode (IO.BCM)

left_IR_pin=23
right_IR_pin=24
IO.setup(left_IR_pin,IO.IN) #blue solve
IO.setup(right_IR_pin,IO.IN) #red solve


while 1:

    if(IO.input(left_IR_pin)==True):
        print("solve left")
    
    if(IO.input(right_IR_pin)==True):
        print("solve right")
