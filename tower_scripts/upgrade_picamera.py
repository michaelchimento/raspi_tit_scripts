from term_utils import *
from ipsandnames import pi_data_table

for pi in pi_data_table:
    print("Updating picamera package in {}".format(pi))
    reachable = ping_pi(pi[1])
	
    if not reachable:
        pass
    else:
        kill_python(pi[1])

        upgrade_python_package(pi[1], "picamera")

        reboot(pi[1])
