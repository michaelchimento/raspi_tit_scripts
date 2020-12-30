from term_utils import *
from all_ipsandnames import pi_data_table

env_pis = [["EnvInfoD4","10.76.0.52"],["EnvInfoC1","10.76.0.53"],["EnvInfoD3","10.76.0.54"],["EnvInfoG10","10.76.0.57"]]

for pi in env_pis:
    print("Copying local ssh key to pi @ {}".format(pi))
    reachable = ping_pi(pi[1])
	
    if not reachable:
        pass
    else:
        response = copy_ssh_id(pi[1])
        print(response)
