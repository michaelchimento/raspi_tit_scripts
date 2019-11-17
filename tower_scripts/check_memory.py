#!/usr/bin/python3

import subprocess
import csv
import datetime as dt
import os
from ipsandnames import pi_data_table

#pi_data_table format is [(pi name1, pi IP1), (pi name2, pi IP2),... etc]
#print(pi_data_table)

def terminal(command):
    term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return term_output.decode()

for pi in pi_data_table:
	print("Checking python processes in {}".format(pi))
	try:
		command = "ping -c2 {}".format(pi[1])
		response = terminal(command)
		if "2 received, 0% packet loss" in response:
			#check to see that 2 python programs are running
			command = "ssh pi@{} df -h".format(pi[1])
			mem_info = terminal(command)
			print(mem_info)
		else:
			print("{} not responding to pings".format(pi[0]))

	except Exception as e:
		print(e)
