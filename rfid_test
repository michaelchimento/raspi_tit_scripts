import time
import serial
import datetime as dt

#run python -m serial.tools.list_ports in terminal to check serial port name

def mof_read(ser):
    print("enter mof")
    ser.write(b"MOF\r")
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
                    id_tag=""
            
            elif(data[-10:] != id_tag and id_tag[-4:] not in data):
                print("displacement")
                time_stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
                id_tag = data
            
            else:
                tolerance_limit = 0
            
    return tag_present, id_tag

ser = serial.Serial('/dev/ttyS0', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
#print(ser)
mof_read(ser)

global tag_present
tag_present = 0
while True:
    if tag_present==0:
        tag_present, id_tag = arrival_check(ser, tag_present)
    elif tag_present==1:
        tag_present, id_tag = depart(ser,tag_present,id_tag)
        


