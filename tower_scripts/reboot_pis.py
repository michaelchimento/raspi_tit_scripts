#!/usr/bin/python3
import datetime as dt
import os
import sys
from all_ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python, reboot, take_test_img

print("####{} reboot_pis.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

for pi in pi_data_table:
    print("pinging {}".format(pi))
    reachable = ping_pi(pi[1])
    if not reachable:
        pass
    else:
        print("rebooting {} {}".format(pi[0],pi[1]))        
        reboot(pi[1])

env_pis = [["EnvInfoD4","10.76.0.52"],["EnvInfoC1","10.76.0.53"],["EnvInfoD3","10.76.0.54"],["EnvInfoG10","10.76.0.57"]]

for pi in env_pis:
    print("pinging {}".format(pi))
    reachable = ping_pi(pi[1])
    if not reachable:
        pass
    else:
        print("rebooting {} {}".format(pi[0],pi[1]))        
        reboot(pi[1])

