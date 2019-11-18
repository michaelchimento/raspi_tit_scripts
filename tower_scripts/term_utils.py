#!/usr/bin/python3

import subprocess

def terminal(command):
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        #uncomment line below for more detailed debugging
        #print("{}: {}".format(e.cmd,e.output.decode()))
        raise e
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
	    
def delete_git(ipaddress):
    command = "ssh pi@{} sudo rm -rf raspi_tit_scripts/".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. See previous output for details.")
    else:
        print(response)

def install_git(ipaddress):
    
    command = "ssh pi@{} git clone https://github.com/michaelchimento/raspi_tit_scripts.git".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. See previous output for details.")
    else:
        print(response)
        
def chmod_launchers(ipaddress,name):
    if "Puzzle" in name:
        launchername = "puzzle_launcher.sh"
    elif "Social" in name:
        launchername = "social_launcher.sh"
    elif "Observ" in name:
        launchername = "observ_launcher.sh"
    elif "Feeder" in name:
        launchername = "feeder_launcher.sh"
        
    command = "ssh pi@{} chmod +x raspi_tit_scripts/launchers/{}".format(ipaddress,launchername)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. See previous output for details.")
    else:
        print(response)
	
def git_pull(ipaddress):
    #update pi's with most recent commit
    command = "ssh pi@{} \"cd raspi_tit_scripts/ && git pull\"".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, git is already up to date.")
    else:
        print(response)
        
def reboot(ipaddress):
    #update pi's with most recent commit
    command = "ssh pi@{} sudo shutdown -r 1".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print("Oops, something's wrong.")
        print(e)
    else:
        print(response)
	
def current_py_processes(ipaddress):
    command = "ssh pi@{} pgrep -af python".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print("Oops, something's wrong. No processes running.")
    else:
        return response
    
