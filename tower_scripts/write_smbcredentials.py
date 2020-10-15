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
        #command = "ssh pi@{} \'\'".format(pi[1])
        #command = "ssh pi@{} mkdir /home/pi/mnt".format(pi[1])
        command = "ssh pi@{} \'set +H;echo -e \"username=mchimento\npassword=***\ndomain=top.orn.mpg.de\" | sudo tee /etc/.smbcredentials;mkdir /home/pi/mnt; echo -e \"//10.0.16.7/grpLucy /home/pi/mnt cifs x-systemd.automount,credentials=/etc/.smbcredentials,uid=pi,gid=pi,vers=3.0 0 0\" | sudo tee -a /etc/fstab\'".format(pi[1])
        try:
            print(command)
            response = terminal(command)
            print(response)
        except Exception as e:
            print("{}, error writing to file".format(e))

        #reboot(pi[1])

