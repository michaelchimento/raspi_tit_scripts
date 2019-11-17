#!/usr/bin/python3
import subprocess
import csv
import datetime as dt
import os
from ipsandnames import pi_data_table

#reads from csv that has col1:names, col2:IP address (no user!)
#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

def terminal(command):
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("Oops, something's wrong:")
        print("{}: {}".format(e.cmd,e.output.decode()))
    else:
        return term_output.decode()

### MOVE VIDEOS TO TRANSFER FOLDER ON PI
for pi in pi_data_table:  #use this for more than one pi
    print("Transferring videos within Pi for {}".format(pi))
    command = "ping -c2 {}".format(pi[1])
    response = terminal(command)
    if response:
        copy_from = "APAPORIS/MOVED/"
        copy_to = "APAPORIS/TO_TRANSFER/"

        #count files
        command = "ssh pi@{} ls {} | wc -l".format(pi[1],copy_from)
        file_count_MOVED = terminal(command)
        
        if int(file_count_MOVED)==0:
            print("no files to move")
            pass
        else:
            print("Moving {} files or folders".format(file_count_MOVED))
            #move files from "moved" to "to_transfer"
            command = 'ssh pi@{} mv {}* {}'.format(pi[1], copy_from, copy_to)
            terminal(command)
   
    else:
        print("{} not responding to pings".format(pi[0]))

### COPY VIDEOS AND CSV TO TOWER/DELETE FROM PI
for pi in pi_data_table:  #use this for more than one pi
    print("Transferring videos from Pi {} to Desktop".format(pi))
    time_stamp = dt.datetime.now().strftime('%Y-%m-%d_%H')
    target_folder = "{}_{}/".format(pi[0],time_stamp)

    command = "ping -c2 {}".format(pi[1])
    response = terminal(command)
    if response:
        copy_from = "APAPORIS/TO_TRANSFER/"
        copy_to = "~/TITS/VIDEOS/{}".format(target_folder)
        file_count_TO_TRANSFER = terminal("ssh pi@{} ls {} | wc -l".format(pi[1],copy_from))
        #make folder on this computer
        if int(file_count_TO_TRANSFER) ==0:
            print("no files to transfer to tower")
            pass
        else:
            if not os.path.isdir(copy_to):
                command= "mkdir -v {}".format(copy_to)
                terminal(command)
        
            #create commands to copy files from pi, feeder and observ pi's require recursive scp command
            if "Puzzle" in pi[0] or "Social" in pi[0]:
                print("Moving {} videos".format(file_count_TO_TRANSFER))
                command = 'scp -p pi@{}:{}* {}'.format(pi[1],copy_from,copy_to)
            else:
                print("Moving {} folders of photos".format(file_count_TO_TRANSFER))
                command = 'scp -rp pi@{}:{}* {}'.format(pi[1],copy_from,copy_to)
            
            #execute move
            terminal(command)
            
            #count files which have been moved
            file_count_TOWER = terminal("ls {} | wc -l".format(copy_to))

            if  file_count_TO_TRANSFER == file_count_TOWER:
                command = 'ssh pi@{} rm -rf {}*'.format(pi[1],copy_from)
                terminal(command)
                print('All files transferred Successfully')
            else:
                print("mismatch between file counts of pi and tower")
                  
    else:
        print("{} interrupted during transfer. Not responding to pings".format(pi[0]))
        break

