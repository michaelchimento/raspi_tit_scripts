#!/usr/bin/python3

import subprocess

def terminal(command):
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        #uncomment line below for more detailed debugging
        #print("{}: {}".format(e.cmd,e.output.decode()))
        raise
    else:
        return term_output.decode()
        
def ping_pi(ipaddress):
    command = "ping -c2 {}".format(ipaddress)
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("Oops, something's wrong: {} is not responding to pings".format(ipaddress))
        return False
    else:
        return True
        
def kill_python(ipaddress):
    #kill all python processes
	command = "ssh pi@{} sudo pkill python".format(ipaddress)
	try:
	    response = terminal(command)
	except Exception:
	    print("0 python scripts running")
	
def git_pull(ipaddress):
    #update pi's with most recent commit
    command = "ssh pi@{} cd raspi_tit_scripts/; git pull".format(ipaddress)
    try:
        response = terminal(command)
    except Exception:
        print("Oops, something's wrong. See previous output for details.")
    else:
        print(response)
        
def reboot(ipaddress):
    #update pi's with most recent commit
    command = "ssh pi@{} sudo reboot".format(ipaddress)
    try:
        response = terminal(command)
    except Exception:
        print("Oops, something's wrong. Uncomment debug line in terminal() for more info")
    else:
        print(response)
	
def current_py_processes(ipaddress):
    command = "ssh pi@{} pgrep -af python".format(ipaddress)
    try:
        response = terminal(command)
    except Exception:
        print("Oops, something's wrong. No processes running.")
    else:
        return response
    
