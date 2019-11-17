#!/usr/bin/python3


from ipsandnames import pi_data_table
from term_utils import terminal, ping_pi, current_py_processes

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

for pi in pi_data_table:
	print("Checking python processes in {}".format(pi))
	reachable = ping_pi(pi[1])
	if not reachable:
	    pass
	else:
		#check to see that 2 python programs are running
		
		py_processes = current_py_processes(pi[1])
		if not py_processes:
		    pass
		else:
		    if "Puzzle" in pi[0] and len(py_processes.split("\n")) == 3:
			    print("Puzzle rfid and video running")
		    elif "Observ" in pi[0] and len(py_processes.split("\n")) == 2:
		        print("Observation network photos running")
		    elif "Feeder" in pi[0] and len(py_processes.split("\n")) == 2:
		        print("Feeder network photos running")
		    elif "Social" in pi[0] and len(py_processes.split("\n")) == 2:
		        print("Social network photos running")
		    else:
			    print("processes running in {}:\n{}".format(pi[0],py_processes))
			    print("problem with one or more processes")

