#!/usr/bin/python3

from ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python, git_pull, reboot, delete_git

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

for pi in pi_data_table:
	print("Updating scripts from Github in {}".format(pi))
	reachable = ping_pi(pi[1])
	
	if not reachable:
	    pass
	else:
	    
	    #stop all python scripts running
	    kill_python(pi[1])
	    
	    #pull latest commit from github
        git_pull(pi[1])
	    
	    reboot(pi[1])
		

