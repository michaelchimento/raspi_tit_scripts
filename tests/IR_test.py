import RPi.GPIO as IO
from rpi_info import name
IO.setwarnings(False)
IO.setmode (IO.BCM)

if "Puzzle_P1" in name:
    left_IR_pin=19
else:
    left_IR_pin=23
    
right_IR_pin=24
IO.setup(left_IR_pin,IO.IN) #blue solve
IO.setup(right_IR_pin,IO.IN) #red solve


while 1:

    if(IO.input(left_IR_pin)==True):
        print("solve left")
    
    if(IO.input(right_IR_pin)==True):
        print("solve right")
