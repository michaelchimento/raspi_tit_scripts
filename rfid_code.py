#!/usr/bin/python3

import time
import socket
import smtplib
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
global scrounge_count
scrounge_count=0
global comp_name
comp_name = socket.gethostname()

class motorThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.email_flag = 0
        self.state = 0
        self.steps = 450
        self.pull_style = stepper.MICROSTEP
        self.kit = MotorKit()

    
    def zero(self):
        global id_tag
        if(IO.input(23)==True):
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
            to_write_list = "{},{},{},{}".format(id_tag,"efficient",time_stamp[0],time_stamp[1])
            write_csv(to_write_list,file_name)
            print("solve right")
            self.state = 1
    
        elif(IO.input(24)==True):
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
            to_write_list = "{},{},{},{}".format(id_tag,"inefficient",time_stamp[0],time_stamp[1])
            write_csv(to_write_list,file_name)
            print("solve left")
            self.state = 1

    def one(self):
        global tag_present
        global scrounge_count
        #print("waiting for scroungers")
        if tag_present==0 or scrounge_count==2:
            self.state = 2
            scrounge_count=0
    
    def two(self):
        time.sleep(1)
        for x in range(self.steps):
            self.kit.stepper1.onestep(direction=stepper.BACKWARD, style=self.pull_style)
        self.kit.stepper1.release()
        time.sleep(1)
        for x in range(self.steps):
            self.kit.stepper1.onestep(direction=stepper.FORWARD, style=self.pull_style)
        self.kit.stepper1.release()
        
        if(IO.input(23)==False and IO.input(24)==False):
            self.email_flag=0
            self.state = 0
        elif((IO.input(23)==True or IO.input(24)==True) and self.email_flag==0):
            user = 'greti.lab.updates@gmail.com'
            password = 'greti2019'
            sent_from = 'greti.lab.updates@gmail.com'
            to = 'mchimento@ab.mpg.de'
            subject = 'critical failure in {}'.format(comp_name)
            body = 'go check'
            email_text = 'From:{}\nTo:{}\nSubject:{}\n{}'.format(sent_from,to,subject,body)
            print(email_text)

            try:
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.ehlo()
                server.starttls()
                server.login(user,password)
                server.sendmail(sent_from, to, email_text)
                server.close()
                self.email_flag=1
                print("Email Sent!")
                
            except:
                print("no worky worky")
        else:
            self.state=2
            
    
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

def write_csv(to_write_list,file_name):
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
    global scrounge_count
    while tag_present==0:
        if ser.inWaiting() > 0:
            id_tag = ser.read_until("\r".encode())[0:-1]
            id_tag = id_tag.decode("latin-1")
            #print(id_tag)
            #print (len(id_tag))
            if len(id_tag)==10:
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                print("{} arrived".format(id_tag[-10:]))
                write_csv("{},{},{},{}".format(id_tag,"arrived",time_stamp[0],time_stamp[1]),file_name)
                if motor_thread.state == 2:
                    print("scrounge attack!")
                    write_csv("{},{},{},{}".format(id_tag,"scrounge",time_stamp[0],time_stamp[1]),file_name)
                    scrounge_count +=1
                tag_present = 1
            else: print("watever")
                    
    return tag_present, id_tag

def depart(ser, tag_present, id_tag):
    
    global scrounge_count
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
                if tolerance_limit >= 3:
                    print("{} left".format(id_tag))
                    tag_present=0
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]),file_name)
                    id_tag=""
            
            elif(data[-10:] != id_tag and id_tag[-4:] not in data):
                print("displacement")
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]),file_name)
                write_csv("{},{},{},{}".format(data[-10:],"displacement",time_stamp[0],time_stamp[1]),file_name)
                if motor_thread.state == 1:
                    print("scrounge attack!")
                    write_csv("{},{},{},{}".format(data[-10:],"scrounge",time_stamp[0],time_stamp[1]),file_name)
                    scrounge_count +=1
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
mof_read(ser)


#set up csv
global file_name
file_name = "/home/pi/Desktop/puzzle_code_pi/data/{}_RFID.csv".format(comp_name)
header = "ID, Event, YMD, Timestamp\n"
time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
savefile = open(file_name, "a") # open data file in write mode
savefile.write("#{} start time: {} \n".format(comp_name,time_stamp))
savefile.write(header)
savefile.close()

motor_thread = motorThread(1, "Motor-Thread")
motor_thread.start()

while True:
    
    if tag_present == 0:
        print("tp: {}".format(tag_present))
        tag_present, id_tag = arrival_check(ser, tag_present)
    elif tag_present == 1:
        print("tp: {}".format(tag_present))
        tag_present, id_tag = depart(ser, tag_present, id_tag)
        
ser.close()
