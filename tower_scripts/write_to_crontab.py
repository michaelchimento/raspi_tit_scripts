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
        command = "echo \"0 6 * * * reboot\n0 * * * * mnt /home/pi/mnt\" | ssh pi@{} sudo crontab -".format(pi[1])
        #command = "echo \"@reboot sh /home/pi/raspi_tit_scripts/launchers/{}_launcher.sh 2 >> /home/pi/raspi_tit_scripts/logs/{}_errorlog\n*/20 * * * * sh /home/pi/raspi_tit_scripts/launchers/upload_files_launcher.sh 2 >> /home/pi/raspi_tit_scripts/logs/upload_errorlog\n0 23 * * * mv APAPORIS/CURRENT/* APAPORIS/MOVED/\" | ssh pi@{} \"crontab -\"".format(pi[0][:6].lower(),pi[0][:6].lower(), pi[1])
        try:
            print(command)
            response = terminal(command)
            print(response)
        except:
            print("error writing to crontab")

        reboot(pi[1])

