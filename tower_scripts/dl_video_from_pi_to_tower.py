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
    term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return term_output.decode()


### MOVE VIDEOS TO TRANSFER FOLDER ON PI
for pi in pi_data_table:  #use this for more than one pi
    print("Transferring videos within Pi for {}".format(pi))
    try:
        command = "ping -c2 {}".format(pi[1])
        response = terminal(command)
        if "2 received, 0% packet loss" in response:
            copy_from = "APAPORIS/MOVED/"
            copy_to = "APAPORIS/TO_TRANSFER/"

            #count files
            command = "ssh pi@{} ls {} | wc -l".format(pi[1],copy_from)
            file_count_copy_from = terminal(command)
            print("Moving files: {}".format(file_count_copy_from))
            #move files from "moved" to "to_transfer"
            command = 'ssh pi@{} mv {}* {}'.format(pi[1], copy_from, copy_to)
            terminal(command)
            
            #count moved files
            file_count_copy_to = terminal("ssh pi@{} ls {} | wc -l".format(pi[1],copy_to))
            
            if file_count_copy_from == file_count_copy_to:
            	print("All files copied")
            else:
            	print("{} interrupted while moving files internally.".format(pi[0]))
       
        else:
            print("{} not responding to pings".format(pi[0]))

    except Exception as e:
        print(e)

### COPY VIDEOS AND CSV TO TOWER/DELETE FROM PI
for pi in pi_data_table:  #use this for more than one pi
    print("Transferring videos from Pi {} to Desktop".format(pi))
    time_stamp = dt.datetime.now().strftime('%Y-%m-%d_%H')
    target_folder = "{}_{}/".format(pi[0],time_stamp)
    try:
        command = "ping -c2 {}".format(pi[1])
        response = terminal(command)
        if "2 received, 0% packet loss" in response:
            copy_from = "APAPORIS/TO_TRANSFER/"
            copy_to = "~/TITS/VIDEOS/{}".format(target_folder)
            file_count_copy_from = terminal("ssh pi@{} ls {} | wc -l".format(pi[1],copy_from))
            #make folder on this computer
            command= "mkdir -v {}".format(copy_to)
            terminal(command)
            
            #copy files from pi
            command = 'scp pi@{}:{}*.* {}'.format(pi[1],copy_from,copy_to)
            terminal(command)
            
            file_count_copy_to = terminal("ls {} | wc -l".format(copy_to))

            if  file_count_copy_from == file_count_copy_to:
                command = 'ssh pi@{} rm -rf {}*'.format(pi[1],copy_from)
                terminal(command)
                print('All files transferred Successfully')
                      
        else:
            print("{} interrupted during transfer. Not responding to pings".format(pi[0]))
            break

    except Exception as e:
         print(e)
