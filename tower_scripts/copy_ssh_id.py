from term_utils import *
from all_ipsandnames import pi_data_table

for pi in pi_data_table:
    print("Copying local ssh key to pi @ {}".format(pi))
    reachable = ping_pi(pi[1])
	
    if not reachable:
        pass
    else:
        response = copy_ssh_id(pi[1])
        print(response)
