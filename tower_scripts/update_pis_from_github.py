#!/usr/bin/python3

from all_ipsandnames import pi_data_table
from term_utils import *

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]

for pi in pi_data_table:
    print("Updating scripts from Github in {}".format(pi))
    reachable = ping_pi(pi[1])
    if not reachable:
        pass
    else:
        kill_python(pi[1])
        git_pull(pi[1])
        chmod_launchers(pi[1],pi[0])
        reboot(pi[1])
		

