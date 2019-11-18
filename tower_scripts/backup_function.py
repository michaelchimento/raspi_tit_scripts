#!/usr/bin/python3

import subprocess
import os
import numpy as np
from term_utils import terminal


#replace this with appropriate local & remote paths for backup
copy_from = "~/TITS/VIDEOS/"
copy_to = "/mnt/Videos_GRETI/field_season_winter_2020/"

if not os.path.exists(copy_to):
    print("mounting drive")
    command = "sudo mount -a"
    terminal(command)

#Get a list of files in original folder
files_from = os.listdir(copy_from)
#Get a list of files in backup folder
files_bup = os.listdir(copy_to)
files_to_bup = np.setdiff1d(files_from, files_bup)

#Copy Video files
print("backing up {} files".format(len(files_to_bup)))
for video in files_to_bup:
    command = 'mv {}{} {}'.format(copy_from,video,copy_to)
    terminal(command)
print("All files backed up")

