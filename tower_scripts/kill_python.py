#!/usr/bin/python3

from all_ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

for pi in pi_data_table:
    print("Killing python processes in {}".format(pi))
    reachable = ping_pi(pi[1])
    if not reachable:
        pass
    else:
        kill_python(pi[1])

