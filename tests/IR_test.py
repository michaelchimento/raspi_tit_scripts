import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(15,IO.IN) #GPIO 15 -> IR sensor as input
IO.setup(18,IO.IN) #GPIO 18 -> IR sensor as input


while 1:

    if(IO.input(15)==False):
        print("solve")
    
    if(IO.input(18)==False):
        print("solve")
