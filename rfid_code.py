import time
import serial
import datetime as dt
import threading
import RPi.GPIO as IO
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(23,IO.IN)
IO.setup(24,IO.IN)

global id_tag
id_tag = ""
global tag_present
tag_present=0

class motorThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.state = 0
        self.steps = 450
        self.pull_style = stepper.MICROSTEP
        self.kit = MotorKit()

    
    def zero(self):
        global id_tag
        if(IO.input(23)==True):
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
            to_write_list = "{},{},{},{}".format(id_tag,"efficient",time_stamp[0],time_stamp[1])
            write_csv(to_write_list)
            print("solve right")
            self.state = 1
    
        elif(IO.input(24)==True):
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
            to_write_list = "{},{},{},{}".format(id_tag,"inefficient",time_stamp[0],time_stamp[1])
            write_csv(to_write_list)
            print("solve left")
            self.state = 1

    def one(self):
        global tag_present
        #print("waiting for scroungers")
        if tag_present==0:
            self.state = 2
    
    def two(self):
        print("motor turn")
        time.sleep(1)
        for x in range(self.steps):
            self.kit.stepper1.onestep(direction=stepper.BACKWARD, style=self.pull_style)
        self.kit.stepper1.release()
        time.sleep(1)
        for x in range(self.steps):
            self.kit.stepper1.onestep(direction=stepper.FORWARD, style=self.pull_style)
        self.kit.stepper1.release()

        self.state = 0
    
    def state_switcher(self, i):
        switcher = {
            0:self.zero,
            1:self.one,
            2:self.two
            }
        func=switcher.get(i, lambda:"Invalid")
        return func()

    def thread_action(self):
        self.state_switcher(self.state)

    def run(self):
        print("Starting " + self.name)
        while 1:
            self.thread_action()
        print("Exiting " + self.name)

motor_thread = motorThread(1, "Motor-Thread")
motor_thread.start()

def write_csv(to_write_list):
    file_name = "P1_RFID.csv"
    savefile = open(file_name, "a")
    savefile.write(to_write_list+"\n")
    savefile.close()

def mof_read(ser):
    ser.write("MOF\r".encode())
    print("MOF")
    time.sleep(2.5)
    while True:
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            print(data)
            return

def arrival_check(ser, tag_present):
    while tag_present==0:
        if ser.inWaiting() > 0:
            id_tag = ser.read_until("\r".encode())[0:-1]
            id_tag = id_tag.decode("latin-1")
            print(id_tag)
            print (len(id_tag))
            if len(id_tag)==10:
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                print("{} arrived".format(id_tag[-10:]))
                write_csv("{},{},{},{}".format(id_tag,"arrived",time_stamp[0],time_stamp[1]))
                if motor_thread.state == 1:
                    print("scrounge attack!")
                    write_csv("{},{},{},{}".format(id_tag,"scrounge",time_stamp[0],time_stamp[1]))
                tag_present = 1
            else: print("watever")
                    
    return tag_present, id_tag

def depart(ser, tag_present, id_tag):
    
    tolerance_limit = 0
    
    while tag_present==1:
        ser.write("RSD\r".encode())
        time.sleep(.2)
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            data = data.decode("latin-1")
            print(data)
            if (data == "?1"):
                tolerance_limit +=1
                if tolerance_limit == 3:
                    tag_present=0
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]))
                    print("bird left")
                    id_tag=""
            
            elif(data[-10:] != id_tag and id_tag[-4:] not in data):
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]))
                write_csv("{},{},{},{}".format(data[-10:],"displacement",time_stamp[0],time_stamp[1]))
                if motor_thread_state == 1:
                    print("scrounge attack!")
                    write_csv("{},{},{},{}".format(data[-10:],"scrounge",time_stamp[0],time_stamp[1]))
                print("displacement")
                id_tag = data
            
            else:
                tolerance_limit = 0
            
    return tag_present, id_tag

#set up serial and read operating frequency
ser = serial.Serial('/dev/ttyS0', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
print(ser)
mof_read(ser)


#set up csv
file_name = "P1_RFID.csv"
header = "ID, Event, YMD, Timestamp\n"
time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
savefile = open(file_name, "a") # open data file in write mode
savefile.write("#start time: "+ time_stamp)
savefile.write(header)
savefile.close()

while True:
    
    if tag_present == 0:
        print("tp: {}".format(tag_present))
        tag_present, id_tag = arrival_check(ser, tag_present)
    elif tag_present == 1:
        print("tp: {}".format(tag_present))
        tag_present, id_tag = depart(ser, tag_present, id_tag)
        
ser.close()
