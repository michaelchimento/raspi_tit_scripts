import subprocess, os, socket
import numpy as np
import datetime as dt
from rpi_info import name
import psutil

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                print("{} is already running".format(proc.name().lower()))
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
     print("{} not running.".format(processName))
     return False;


def terminal(command):
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        #uncomment line below for more detailed debugging
        #print("{}: {}".format(e.cmd,e.output.decode()))
        raise e
    else:
        return term_output.decode()

##replace this with appropriate local & remote paths for backup
copy_from = "/home/pi/APAPORIS/MOVED/"
copy_to = "/home/pi/mnt/Videos_GRETI/field_season_fall_2020/{}".format(name)

def backup_to_server():
    print("####{} backup_function.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))
    #Get a list of files in original folder
    files_from = os.listdir(copy_from)
    #Get a list of files in backup folder
    files_bup = os.listdir(copy_to)
    files_to_bup = np.setdiff1d(files_from, files_bup)

    #Copy Video files
    print("backing up {} files".format(len(files_to_bup)))
    for video in files_to_bup:
        try:
            command = 'mv {}{} {}'.format(copy_from,video,copy_to)
            terminal(command)
        except Exception as e:
            print(e)
            print("Error uploading {} to server. Uploading to overflow folder to avoid merge error.".format(video))
            try:            
                command = 'mv {}{} {}_overflow/'.format(copy_from,video,copy_to)
                print(command)
                terminal(command)
            except Exception as e:
                print("A further error has occurred. Manually remove files to save data.")
        else:
            print("{} backed up".format(video))

if not checkIfProcessRunning("upload_to_server2020.py"):
    if not os.path.isdir(copy_to):     
        os.mkdir(copy_to)

    backup_to_server()
