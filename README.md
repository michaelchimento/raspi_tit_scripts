# raspi_tit_scripts
repo for aviary raspi scripts and tests
```
#################################################################
# ______       _______                   ||==================...#
#|big   |      |tower|                   ||  pi  pi  pi  pi     #
#|ass   |      |     |                   ||    aviaries         #
#|server|      |     |     network cxn   ||  pi  pi  pi  pi     #
#|______|======|_____|= = = = = = = = = =||==================...#
#################################################################
```
For installation on Pis:
run  ```python3 fresh_install_pi.py``` from the tower
and then run ```python3 write_to_crontab.py``` with desired jobs
OR

SSH into pi,

clone repo to home directory,

ensure ```chmod +x``` for files in "launchers" directory

After either option, add the following (or whatever you so desire) to crontab:
```bash
@reboot sh /home/pi/raspi_tit_scripts/launchers/**CORRECTVERSION**_launcher.sh 2 >> /home/pi/raspi_tit_scripts/logs/puzzle_errorlog
*/20 * * * * sh /home/pi/raspi_tit_scripts/launchers/upload_files_launcher.sh 2 >> /home/pi/raspi_tit_scripts/logs/upload_errorlog
```
make directory structure ```~/APAPORIS/CURRENT ~/APAPORIS/MOVED ~/APAPORIS/TO_TRANSFER```

Make sure that the List_of_Cameras is kept up to date with pi name, IP address

Also double-check the mount points for the server

for installation on tower, add the following to crontab:
```
00 07 * * * ~/raspi_tit_scripts/launchers/check_ok_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
00 10 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
00 15 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
00 20 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
```

To monitor live puzzles, ssh into pi and run ```tail -F <path to repo>/logs```. the python programs are run by launchers with -u flag to leave stdout unbuffered. Use tmux to keep everything in one place.
