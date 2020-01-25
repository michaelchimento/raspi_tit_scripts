#!/usr/bin/python3

import subprocess
import os
import numpy as np
from term_utils import terminal
import datetime as dt

print("####{} backup_function.py####".format(dt.datetime.now().strftime('%Y-%m-%d_%H_%M')))

#replace this with appropriate local & remote paths for backup
copy_from = "../../TITS/VIDEOS/"
copy_to = "/run/user/1001/gvfs/smb-share:server=r-zfssvr01,share=grplucy/Videos_GRETI"


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
        print("Error uploading {} to server".format(video)
print("All files backed up")

