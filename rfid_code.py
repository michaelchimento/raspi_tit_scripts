#!/usr/bin/python3

import time
import socket
import smtplib
import serial
import datetime as dt
import threading
import RPi.GPIO as IO
import os
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from rpi_info import name
IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(23,IO.IN)
IO.setup(24,IO.IN)

global id_tag
id_tag = ""
global tag_present
tag_present=0
global comp_name
comp_name = name

def send_email():
    user = 'greti.lab.updates@gmail.com'
    password = 'greti2019'
    sent_from = 'greti.lab.updates@gmail.com'
    to = 'mchimento@ab.mpg.de'
    subject = 'door stuck in {}'.format(comp_name)
    body = 'pls help'
    email_text = 'From:{}\nTo:{}\nSubject:{}\n{}'.format(sent_from,to,subject,body)
    #print(email_text)

    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(user,password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        #print("Email Sent!")
        return 0,1
        
    except:
        #print("error with email")
        return 0,0

class motorThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.email_flag = 0
        self.state = 0
        if "P10" in name or "P3" in name:
            self.steps = 500
        else:
            print("normal steps assigned")            
            self.steps = 400
        self.pull_style = stepper.MICROSTEP
        self.kit = MotorKit()
        self.end_time = time.time()

    def zero(self):
        if tag_present:
            if(IO.input(23)==True):
                time.sleep(.2)
                if(IO.input(23)==True):
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    to_write_list = "{},{},{},{}".format(id_tag,"efficient",time_stamp[0],time_stamp[1])
                    write_csv(to_write_list,file_name)
                    print("solve efficient by {}".format(id_tag))
                    self.state = 3
        
            elif(IO.input(24)==True):
                time.sleep(.2)
                if(IO.input(24)==True):
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    to_write_list = "{},{},{},{}".format(id_tag,"inefficient",time_stamp[0],time_stamp[1])
                    write_csv(to_write_list,file_name)
                    print("solve inefficient by {}".format(id_tag))
                    self.state = 3

        elif not tag_present:
            if(IO.input(23)==True):
                time.sleep(.5)
                if(IO.input(23)==True):
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    to_write_list = "{},{},{},{}".format(id_tag,"efficient",time_stamp[0],time_stamp[1])
                    write_csv(to_write_list,file_name)
                    print("solve efficient by {}".format(id_tag))
                    self.state = 3
        
            elif(IO.input(24)==True):
                time.sleep(.5)
                if(IO.input(24)==True):
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    to_write_list = "{},{},{},{}".format(id_tag,"inefficient",time_stamp[0],time_stamp[1])
                    write_csv(to_write_list,file_name)
                    print("solve inefficient by {}".format(id_tag))
                    self.state = 3
                    
            
        else:
            self.state = 0

    def one(self):
        if time.time() < self.end_time:
            #print("waiting for scroungers")
            pass
        else:
            print("scrounge stage complete")
            self.state = 2
            
    
    def two(self):
        print("motors moving")
        for x in range(self.steps):
            self.kit.stepper1.onestep(direction=stepper.BACKWARD, style=self.pull_style)
        self.kit.stepper1.release()
        time.sleep(1)
        for x in range(self.steps):
            self.kit.stepper1.onestep(direction=stepper.FORWARD, style=self.pull_style)
        self.kit.stepper1.release()
        time.sleep(1)
        
        if(IO.input(23)==False and IO.input(24)==False):
            self.email_flag=0
            self.state = 0
        
        elif((IO.input(23)==True or IO.input(24)==True) and self.email_flag==0):
            time.sleep(.5)
            if((IO.input(23)==True or IO.input(24)==True)):
                #self.state, self.email_flag = send_email()
                pass
            else:
                self.state = 0
        else:
            self.state=2
            
    def three(self):
        #this state sets the timer for scrounging, set at 1 second
        print("set time to wait for scroungers")        
        self.end_time = time.time() + 2
        self.state = 1
        
    
    def state_switcher(self, i):
        switcher = {
            0:self.zero,
            1:self.one,
            2:self.two,
            3:self.three
            }
        func=switcher.get(i, lambda:"Invalid")
        return func()

    def thread_action(self):
        self.state_switcher(self.state)

    def run(self):
        #print("Starting " + self.name)
        while 1:
            self.thread_action()
        #print("Exiting " + self.name)

def write_csv(to_write_list,file_name):
    with open(file_name, "a") as savefile:
        savefile.write(to_write_list+"\n")

def sd0_send(ser):
    ser.write("SD0\r".encode())
    print("SD0")
    time.sleep(2.5)
    while True:
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            print(data)
            return

def mof_read(ser):
    ser.write("MOF\r".encode())
    print("MOF")
    time.sleep(2.5)
    while True:
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            print(data)
            return

def arrival_check(ser):
 
    global id_tag
    global tag_present
    while tag_present==0:
        if ser.inWaiting() > 0:
            id_tag = ser.read_until("\r".encode())[0:-1]
            id_tag = id_tag.decode("latin-1")
            if len(id_tag)==10:
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                print("{} arrived".format(id_tag[-10:]))
                write_csv("{},{},{},{}".format(id_tag,"arrived",time_stamp[0],time_stamp[1]),file_name)
                if motor_thread.state == 1:
                    print("scrounge attack! motor_state_1")
                    write_csv("{},{},{},{}".format(id_tag,"scrounge",time_stamp[0],time_stamp[1]),file_name)
                tag_present = 1
            else: 
                                
                print("ID not valid")
                pass

def depart(ser):
    global id_tag
    global tag_present
    tolerance_limit = 0
    
    while tag_present==1:
        ser.write("RSD\r".encode())
        time.sleep(.2)
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            data = data.decode("latin-1")
            ##print(data)
            if (data == "?1"):
                tolerance_limit +=1
                if tolerance_limit >= 4:
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
                    print("scrounge attack! motor_state_1")
                    write_csv("{},{},{},{}".format(data[-10:],"scrounge",time_stamp[0],time_stamp[1]),file_name)
                id_tag = data
            
            else:
                tolerance_limit = 0

#set up serial and read operating frequency
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,  
                    bytesize=serial.EIGHTBITS
                    )
sd0_send(ser)

mof_read(ser)


#set up csv
if not os.path.exists("data/"):
        os.makedirs("data/")

#set file_name and timestamp for start of csv
global file_name
file_name = "data/{}_RFID.csv".format(comp_name)
time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if not os.path.isfile(file_name):
    with open(file_name, "a") as savefile:
        header = "ID, Event, YMD, Timestamp\n"
        savefile.write("#{} start time: {} \n".format(comp_name,time_stamp))
        savefile.write(header)
else:
    with open(file_name, "a") as savefile: # open data file in write mode
        savefile.write("#{} start time: {} \n".format(comp_name,time_stamp))

#begin running motor threads
motor_thread = motorThread(1, "Motor-Thread")
motor_thread.start()

while True:
    
    if tag_present == 0:
        print("tp: {}".format(tag_present))
        arrival_check(ser)
    elif tag_present == 1:
        print("tp: {}".format(tag_present))
        depart(ser)
        
ser.close()
