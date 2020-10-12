import subprocess, os, socket
import numpy as np
from term_utils import terminal
import datetime as dt

def backup_to_server():
    print("####{} backup_function.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))
    ##replace this with appropriate local & remote paths for backup
    copy_from = "/home/pi/APAPORIS/MOVED/"
    copy_to = "/home/pi/mnt/Videos_GRETI/field_season_fall_2020/"
    
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
                command = 'mv {}{} {}overflow/'.format(copy_from,video,copy_to)
                print(command)
                terminal(command)
            except Exception as e:
                print("A further error has occurred. Manually remove files to save data.")
        else:
            print("{} backed up".format(video))
            
backup_to_server()