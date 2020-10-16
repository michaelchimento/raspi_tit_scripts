#!/usr/bin/python3

import subprocess

#general function that sends a command to the terminal, returns str of stout, or raises error


def upgrade_python_package(ipaddress, package):
    command = "ssh pi@{} sudo pip3 install {} --upgrade".format(ipaddress,package)
    try:
        response = terminal(command)
    except Exception as e:
        print("Oops, something's wrong. Couldn't upgrade picamera.")
    else:
        print("updated {}".format(package))        
        return response

def copy_ssh_id(ipaddress):
    command = "ssh-copy-id pi@{}".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print("Oops, something's wrong. Couldn't copy id.")
    else:
        print("Successfully copied ssh key to {}".format(ipaddress))        
        return response

def terminal(command):
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        #uncomment line below for more detailed debugging
        #print("{}: {}".format(e.cmd,e.output.decode()))
        raise e
    else:
        return term_output.decode()

#pings the pi's to ensure they are reachable by ssh. returns boolean
def ping_pi(ipaddress):
    command = "ping -c2 {}".format(ipaddress)
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("Oops, something's wrong: {} is not responding to pings".format(ipaddress))
        return False
    else:
        return True

#returns the currently running python processes
def current_py_processes(ipaddress):
    command = "ssh pi@{} pgrep -af python".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print("Oops, something's wrong. No processes running.")
    else:
        return response

#if running, terminates all python scripts
def kill_python(ipaddress):
    #kill all python processes
	command = "ssh pi@{} sudo pkill python".format(ipaddress)
	try:
	    response = terminal(command)
	except Exception:
	    print("0 python scripts running")

def mem_check(ipaddress):
    #reads %used line from df cmd
    command = "ssh pi@{} df | awk ".format(ipaddress) + "'/\/dev\/root/{print $5}'"
       
    try:
        mem_info = terminal(command)
    except Exception:
        print("error retrieving memory capacity")
    else:
        #print("{} has {} of memory full.".format(ipaddress,mem_info.rstrip()))
        return mem_info.rstrip().replace("%","")

#deletes cloned github repository on pi
def delete_git(ipaddress):
    command = "ssh pi@{} sudo rm -rf raspi_tit_scripts/".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. See previous output for details.")
    else:
        print("Deleted old git repository")

#clears out all files in apaporis directory
def clear_apaporis(ipaddress):
    command = "ssh pi@{}".format(ipaddress) + " \"sudo rm -rf APAPORIS/ && mkdir -p APAPORIS/{CURRENT,MOVED,TO_TRANSFER}\""
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. Issue deleting apaporis.")
    else:
        print("rebuilt apaporis")       
        print(response)

def remove_pycache(ipaddress):
#clears out all files in apaporis directory
    command = "ssh pi@{}".format(ipaddress) + " rm -rf raspi_tit_scripts/__pycache__"
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. Issue deleting pycache.")
    else:
        print("removed pycache")       
        print(response)

def remove_logs(ipaddress):
#clears out all files in apaporis directory
    command = "ssh pi@{}".format(ipaddress) + " rm raspi_tit_scripts/logs"
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. Issue deleting logs.")
    else:
        print("removed log file")       
        print(response)

#does a fresh install of repository from github
def install_git(ipaddress):
    
    command = "ssh pi@{} git clone https://github.com/michaelchimento/raspi_tit_scripts.git".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. See previous output for details.")
    else:
        print("Git cloned repository")        
        print(response)

#essential to run if a fresh install. make sure launchers are executable
def chmod_launchers(ipaddress,name):
    if "Puzzle" in name:
        launchername = "puzzle_launcher.sh"
    elif "Social" in name:
        launchername = "social_launcher.sh"
    elif "Observ" in name:
        launchername = "observ_launcher.sh"
    elif "Feeder" in name:
        launchername = "feeder_launcher.sh"
        
    command = "ssh pi@{} \'chmod +x raspi_tit_scripts/launchers/{};chmod +x raspi_tit_scripts/launchers/upload_files_launcher.sh\'".format(ipaddress,launchername)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, something's wrong. See previous output for details.")
    else:
        print(response)

#pulls most recent commit, updating repository on pi
def git_pull(ipaddress):
    #update pi's with most recent commit
    command = "ssh pi@{} \"cd raspi_tit_scripts/ && git checkout -- . && git pull\"".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print(e)
        print("Oops, git is already up to date.")
    else:
        print(response)

#schedules shutdown of pi's . Essential if python processes are killed
def reboot(ipaddress):
    #update pi's with most recent commit
    command = "ssh pi@{} sudo shutdown -r now".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print("Oops, something went wrong while shutting down.")
        print(e)
    else:
        print(response)

#schedules shutdown of pi's . Essential if python processes are killed
def take_test_img(ipaddress):
    #update pi's with most recent commit
    command = "ssh pi@{} raspistill -o test.jpg".format(ipaddress)
    try:
        response = terminal(command)
    except Exception as e:
        print("Oops, something went wrong while taking a photo.")
        print(e)
    else:
        print(response)

    
