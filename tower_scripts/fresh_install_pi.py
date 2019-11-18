#!/usr/bin/python3

from ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python, git_pull, reboot, delete_git, install_git, chmod_launchers, clear_apaporis

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

for pi in pi_data_table:
    print("Updating scripts from Github in {}".format(pi))
    reachable = ping_pi(pi[1])
	
    if not reachable:
        pass
    else:
        kill_python(pi[1])

        clear_apaporis(pi[1])
	    
        delete_git(pi[1])
	    
        install_git(pi[1])
	    
        chmod_launchers(pi[1],pi[0])
	    
        reboot(pi[1])
