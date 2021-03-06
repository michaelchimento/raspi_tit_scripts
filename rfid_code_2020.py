#!/usr/bin/python3

import time, socket, smtplib, serial, threading, os
import datetime as dt
import RPi.GPIO as IO
from sigterm_exception import *
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

def tprint(*args):
    timestamp = dt.datetime.now().strftime("%b-%d | %H:%M:%S")
    print(timestamp, *args)

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
        if "P10" in comp_name or "P3" in comp_name:
            print("long steps assigned")
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
                    tprint("solve efficient by {}".format(id_tag))
                    self.state = 3
        
            elif(IO.input(24)==True):
                time.sleep(.2)
                if(IO.input(24)==True):
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    to_write_list = "{},{},{},{}".format(id_tag,"inefficient",time_stamp[0],time_stamp[1])
                    write_csv(to_write_list,file_name)
                    tprint("solve inefficient by {}".format(id_tag))
                    self.state = 3

        elif not tag_present:
            if(IO.input(23)==True or IO.input(24)==True):
                time.sleep(.3)
                self.state = 4         
        else:
            self.state = 0

    def one(self):
        if time.time() < self.end_time:
            #print("waiting for scroungers")
            pass
        else:
            tprint("scrounge stage complete")
            self.state = 2
            
    
    def two(self):
        tprint("motors moving")
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
        #this state sets the timer for scrounging, set at 3 seconds
        tprint("set time to wait for scroungers")        
        self.end_time = time.time() + 3
        self.state = 1

    def four(self):
        if(IO.input(23)==True):
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
            to_write_list = "{},{},{},{}".format(id_tag,"efficient",time_stamp[0],time_stamp[1])
            write_csv(to_write_list,file_name)
            tprint("solve efficient by {}".format(id_tag))
            self.state = 3

        elif(IO.input(24)==True):
            time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
            to_write_list = "{},{},{},{}".format(id_tag,"inefficient",time_stamp[0],time_stamp[1])
            write_csv(to_write_list,file_name)
            tprint("solve inefficient by {}".format(id_tag))
            self.state = 3
        
    
    def state_switcher(self, i):
        switcher = {
            0:self.zero,
            1:self.one,
            2:self.two,
            3:self.three,
            4:self.four
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

def arrival_check(ser):
 
    global id_tag
    global tag_present
    while tag_present==0:
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            data = data.decode("latin-1")
            data = data[-10:]
            if len(data)==10:
                id_tag = data[-10:]
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                tprint("{} arrived".format(id_tag))
                write_csv("{},{},{},{}".format(id_tag,"arrived",time_stamp[0],time_stamp[1]),file_name)
                if motor_thread.state == 1 or motor_thread.state == 2:
                    tprint("scrounge attack by {}!".format(id_tag))
                    write_csv("{},{},{},{}".format(id_tag,"scrounge",time_stamp[0],time_stamp[1]),file_name)
                tag_present = 1
            else:
                #print("ID not valid")
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
            data = data[-10:]
            if (data == "?1"):
                tolerance_limit +=1
                if tolerance_limit >= 5:
                    tprint("{} left".format(id_tag))
                    tag_present=0
                    time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                    write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]),file_name)
                    id_tag=""
            
            elif(len(data)==10 and data[-4:] not in id_tag):
                tprint("displacement by {}".format(data))
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]),file_name)
                id_tag = data
                write_csv("{},{},{},{}".format(id_tag,"displacement",time_stamp[0],time_stamp[1]),file_name)
                if motor_thread.state == 1 or motor_thread.state == 2:
                    tprint("scrounge attack by {}!".format(id_tag))
                    write_csv("{},{},{},{}".format(data[-10:],"scrounge",time_stamp[0],time_stamp[1]),file_name)
            
            else:
                tolerance_limit = 0


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

#set up serial and read operating frequency
def create_serial_cxn():
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,  
                        bytesize=serial.EIGHTBITS)
    return ser

if __name__=="__main__":
    ser = create_serial_cxn()
    sd0_send(ser)
    mof_read(ser)

    #set up csv
    if not os.path.exists("data/"):
            os.makedirs("data/")

    #set file_name and timestamp for start of csv
    global file_name
    file_name = "data/{}_RFID_grace.csv".format(comp_name)
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

    #signal.signal(signal.SIGTERM, signal_handler)

    while True:
        if tag_present == 0:
            arrival_check(ser)
        elif tag_present == 1:
            depart(ser)

