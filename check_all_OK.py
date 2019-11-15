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

#clear out yesterday's photos
copy_to = "~/TITS/daily_check/"
command = 'rm -rf {}*.bmp'.format(copy_to)
terminal(command)


for pi in pi_data_table:
	print("Checking python processes in {}".format(pi))
	try:
		command = "ping -c2 {}".format(pi[1])
		response = terminal(command)
		if "2 received, 0% packet loss" in response:
			#check to see that 2 python programs are running
			command = "ssh pi@{} pgrep -af python".format(pi[1])
			py_processes = terminal(command)
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
            
            #download pictures from all pis to local directory for overview
			if "Puzzle" in pi[0] or "Social" in pi[0]:
			    copy_from = "APAPORIS/CURRENT/debug.bmp"
			    command = 'scp pi@{}:{} {}{}.bmp'.format(pi[1],copy_from,copy_to,pi[0])
			    terminal(command)
	
		else:
			print("{} not responding to pings".format(pi[0]))

	except Exception as e:
		print(e)
