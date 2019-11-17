#!/usr/bin/python3

import subprocess
import csv
import datetime as dt
import os
from ipsandnames import pi_data_table

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

def terminal(command):
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("Oops, something's wrong:")
        print("{}: {}".format(e.cmd,e.output.decode()))
    else:
        return term_output.decode()

for pi in pi_data_table:
	print("Checking python processes in {}".format(pi))
	command = "ping -c2 {}".format(pi[1])
	response = terminal(command)
	if response:
		#reads %used line from df cmd
		command = "ssh pi@{} df | awk ".format(pi[1]) + "'/\/dev\/root/{print $5}'"
		mem_info = terminal(command)
		print("{} has {} of memory full.".format(pi[0],mem_info.rstrip()))
	else:
		print("{} not responding to pings".format(pi[0]))

