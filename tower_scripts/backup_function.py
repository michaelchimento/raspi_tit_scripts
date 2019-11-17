#!/usr/bin/python3

import subprocess
import os
import numpy as np

def terminal(command):
    response = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return response.decode()

#replace this with appropriate local & remote paths for backup
copy_from = "/home/michael/TITS/VIDEOS/"
copy_to = "/run/user/1000/gvfs/smb-share:server=r-zfssvr01.top.orn.mpg.de,share=grplucy/Videos_GRETI/field_season_winter_2020/"

#Get a list of files in original folder
files_from = os.listdir(copy_from)
#Get a list of files in backup folder
files_bup = os.listdir(copy_to)
files_to_bup = np.setdiff1d(files_from, files_bup)

#Copy Video files
for video in files_to_bup:
    command = 'mv {}{} {}'.format(copy_from,video,copy_to)
    terminal(command)
print("All files backed up")

