#!/usr/bin/python3
import datetime as dt
import os
import sys
from all_ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python, reboot, take_test_img

print("####{} write_to_crontab.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

for pi in pi_data_table:
    print("Writing to crontab for {}".format(pi))
    reachable = ping_pi(pi[1])
	
    if not reachable:
        pass
    else:
        command = "echo \"@reboot sh /home/pi/raspi_tit_scripts/launchers/{}_launcher.sh > /home/pi/raspi_tit_scripts/logs 2>&1\n00 6 * * * sudo reboot\" | ssh pi@{} \"crontab -\"".format(pi[0][:6].lower(), pi[1])
        try:
            print(command)      
            response = terminal(command)
            print(response)
            
        except:
            print("error writing to crontab")

        reboot(pi[1])
