#!/usr/bin/python3
import subprocess
import csv
import datetime as dt
import os
from ipsandnames import pi_data_table
from term_utils import terminal, ping_pi
from mb_backup_function import *

#reads from csv that has col1:names, col2:IP address (no user!)
#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
print("####{} dl_video_from_pi_to_tower.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

### MOVE VIDEOS TO TRANSFER FOLDER ON PI

for pi in pi_data_table:  #use this for more than one pi
    print("Transferring videos within Pi for {}".format(pi))
    reachable = ping_pi(pi[1])
    if not reachable:
        print("{} not responding to pings".format(pi[0]))
    else:
        copy_from = "APAPORIS/MOVED/"
        copy_to = "APAPORIS/TO_TRANSFER/"

        #count files
        try:
            command = "ssh pi@{} ls {} | wc -l".format(pi[1],copy_from)
            file_count_MOVED = terminal(command)
        except Exception as e:
            print("Error counting number of files in moved")
            file_count_MOVED = 0
            print(e)
        
        if int(file_count_MOVED)==0:
            print("no files to move")
        else:
            print("Attempting to move {} files or folders".format(file_count_MOVED))
            #move files from "moved" to "to_transfer"
            try:
                command = 'ssh pi@{} mv {}* {}'.format(pi[1], copy_from, copy_to)
                terminal(command)
            except Exception as e:
                print("Unable to move files from MOVED to TO_TRANSFER")
                print(e)

print("***Finished moving files on pis, now moving from Pi to Tower***")

counter = 1
### COPY VIDEOS AND CSV TO TOWER/DELETE FROM PI
for pi in pi_data_table:  #use this for more than one pi
    time_stamp = dt.datetime.now().strftime('%Y-%m-%d_%H')
    target_folder = "{}_{}/".format(pi[0],time_stamp)
    copy_from = "APAPORIS/TO_TRANSFER/"
    copy_to = "~/TITS/VIDEOS/{}".format(target_folder)
    
    reachable = ping_pi(pi[1])
    if not reachable:
        print("{} not responding to pings".format(pi[0]))
    else:
        print("Transferring videos from Pi {} to Desktop".format(pi))
        command = "ssh pi@{} ls {} | wc -l".format(pi[1],copy_from)
        file_count_TO_TRANSFER = terminal(command)
        
        if int(file_count_TO_TRANSFER) == 0:
            print("no files to transfer to tower")
        else:
            #make folder on this computer if doesn't exist
            if not os.path.isdir(copy_to):
                print("creating folder {}".format(copy_to))
                try:
                    command= "mkdir -v {}".format(copy_to)
                    terminal(command)
                except:
                    print("error making new directory on computer")
        
            #create commands to copy files from pi, feeder and observ pi's require recursive scp command
            if "Puzzle" in pi[0]:
                print("Moving {} videos".format(file_count_TO_TRANSFER.rstrip()))
                command = 'scp -p pi@{}:{}* {}'.format(pi[1],copy_from,copy_to)
            else:
                print("Moving {} folders of photos".format(file_count_TO_TRANSFER.rstrip()))
                command = 'scp -rp pi@{}:{}* {}'.format(pi[1],copy_from,copy_to)
            
            #execute move
            try:
                terminal(command)
            except Exception as e:
                print("Unable to move video or folder")
                print(e)
            
            #count files which have been moved
            command = "ls {} | wc -l".format(copy_to)
            file_count_TOWER = terminal(command)

            if  file_count_TO_TRANSFER == file_count_TOWER:
                command = 'ssh pi@{} rm -rf {}*'.format(pi[1],copy_from)
                terminal(command)
                print('All files transferred Successfully')
            else:
                print("mismatch between file counts of pi and tower")

            if counter % 3 == 0:
                backup_to_server()
            counter +=1

