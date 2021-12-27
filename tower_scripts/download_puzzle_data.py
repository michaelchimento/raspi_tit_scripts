#!/usr/bin/python3
import datetime as dt
import os
import re
import sys
from all_ipsandnames import pi_data_table
from term_utils import ping_pi, terminal, kill_python, reboot, take_test_img

print("####{} download_puzzle_data.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

#clear out yesterday's photos
destination = "~/ownCloud/data_analysis/exp2_immigration/data/puzzle_data"
source = "~/raspi_tit_scripts/data/*"

for pi in pi_data_table:
    if "Puzzle" in pi[0]:
        target_pop = re.search("P\d?\d", pi[0]).group(0)
        print("Downloading puzzle data from {}".format(target_pop))
        reachable = ping_pi(pi[1])
        if not reachable:
            pass
        else:
            try:
                copy_to= "{}/{}".format(destination,target_pop)
                command = 'rsync -a --exclude \'*.md\' pi@{}:{} {}'.format(pi[1], source, copy_to)
                print(command)
                terminal(command)
            except Exception as e:
                print("Error moving files: {}".format(e))                
                pass
    else:
        pass


env_pis = [["EnvInfoD4","10.76.0.52"],["EnvInfoC1","10.76.0.53"],["EnvInfoD3","10.76.0.54"],["EnvInfoG10","10.76.0.57"]]

destination = "~/TITS/env_data_winter"
source = "~/env_info_code/data/*"

for pi in env_pis:
    print("downloading env data {}".format(pi))
    reachable = ping_pi(pi[1])
    if not reachable:
        pass
    else:
        try:
            copy_to= "{}/{}".format(destination,pi[0])
            command = 'rsync -a --exclude \'*.md\' pi@{}:{} {}'.format(pi[1], source, copy_to)
            print(command)
            terminal(command)
        except Exception as e:
            print("Error moving files: {}".format(e))                
            pass



