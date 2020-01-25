#!/usr/bin/python3
import datetime as dt
import os
import sys
from ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python, reboot, take_test_img

print("####{} get_test_img.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

#clear out yesterday's photos
copy_to = "~/TITS/puzzle_data"
copy_from = "~/raspi_tit_scripts/data"

for pi in pi_data_table:
    if "Puzzle" in pi[0]:
        print("Downloading puzzle data from {}".format(pi))
        reachable = ping_pi(pi[1])
        if not reachable:
            pass
        else:
            try:
                command = 'scp -r pi@{}:{} {}/{}_RFID_{}'.format(pi[1], copy_from, copy_to,pi[0], dt.datetime.now().strftime('%Y-%m-%d_%H_%M'))
                print(command)
                terminal(command)
            except:
                print("nothing in MOVED folder to scp")                
                pass
    else:
        pass





