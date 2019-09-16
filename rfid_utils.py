import time
import datetime as dt
import threading
import RPi.GPIO as IO


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
                tag_present = 1
            else: print("watever")
                    
    return tag_present, id_tag

def depart(ser, tag_present, id_tag):
    while tag_present==1:
        ser.write("RSD\r".encode())
        print("rsd")
        time.sleep(.2)
        if ser.inWaiting() > 0:
            data = ser.read_until("\r".encode())[0:-1]
            data = data.decode("latin-1")
            print(data)
            if (data == "?1"):
                tag_present=0
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]))
                print("bird left")
            
            elif(data[-10:] != id_tag and id_tag[-4:] not in data):
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                write_csv("{},{},{},{}".format(id_tag,"departed",time_stamp[0],time_stamp[1]))
                write_csv("{},{},{},{}".format(data[-10:],"displacement",time_stamp[0],time_stamp[1]))
                print("displacement")
                id_tag = data
            
    return tag_present, id_tag

class motorThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.state = 0
    
    def zero(self):
        if(IO.input(23)==False):
            to_write_list = "{},{},{},{}".format(" ")
            write_csv(to_write_list)
            print("solve right")
            self.state = 1
    
        elif(IO.input(24)==False):
            print("solve left")
            self.state = 1

    def one(self):
        print("motor turn")
        time.sleep(1)
        self.state = 0
    
    def state_switcher(self, i):
        switcher = {
            0:self.zero,
            1:self.one
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
