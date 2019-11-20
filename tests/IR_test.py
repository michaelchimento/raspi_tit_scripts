import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(23,IO.IN) #GPIO 23 -> IR sensor as input
IO.setup(24,IO.IN) #GPIO 24 -> IR sensor as input


while 1:

    if(IO.input(23)==True):
        print("solve efficient")
    
    if(IO.input(24)==True):
        print("solve inefficient")
