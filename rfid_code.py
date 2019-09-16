import time
import serial
import rfid_utils as rf
import datetime as dt
global tag_present
import threading
import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(23,IO.IN)
IO.setup(24,IO.IN)



#set up serial and read operating frequency
ser = serial.Serial('/dev/ttyS0', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
print(ser)
rf.mof_read(ser)


#set up csv
file_name = "P1_RFID.csv"
savefile = open(file_name, "a") # open data file in write mode
header = "ID, Event, YMD, Timestamp\n"
savefile.write(header)
savefile.close()


global tag_present
tag_present=0

thread1 = rf.motorThread(1, "Motor-Thread")
thread1.start()

while True:
    
    if tag_present == 0:
        print("tp: {}".format(tag_present))
        tag_present, id_tag = rf.arrival_check(ser, tag_present)
    elif tag_present == 1:
        print("tp: {}".format(tag_present))
        tag_present, id_tag = rf.depart(ser, tag_present, id_tag)
        
ser.close()
