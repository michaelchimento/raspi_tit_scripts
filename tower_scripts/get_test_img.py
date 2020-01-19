#!/usr/bin/python3
import datetime as dt
import os
import sys
from ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python, reboot, take_test_img

print("####{} get_test_img.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

#clear out yesterday's photos
copy_to = "~/TITS/daily_check"
copy_from = "APAPORIS/MOVED"
command = 'rm -rf {}/*.jpg'.format(copy_to)
terminal(command)

for pi in pi_data_table:
    print("Attempting to take picture from {}".format(pi))
    reachable = ping_pi(pi[1])
	
    if not reachable:
        pass
    else:
        if "Puzzle" not in pi[0]:
            #return most recently created image
            command = "ssh pi@{} \"cd {} && ls -t | head -n1\"".format(pi[1],copy_from)
            print(command)
            most_recent_folder = terminal(command).strip(" \n")
            print(most_recent_folder)
            command = "ssh pi@{} \"cd {}/{} && ls -t | head -n1\"".format(pi[1],copy_from,most_recent_folder)
            print(command)
            most_recent_img = terminal(command).strip()
            print(most_recent_img)
            #copy to tower
            try:
                command = 'scp pi@{}:{}/{}/{} {}/{}.jpg'.format(pi[1], copy_from,most_recent_folder,most_recent_img, copy_to,pi[0])
                print(command)
                terminal(command)
            except:
                print("nothing in MOVED folder to scp")                
                pass





