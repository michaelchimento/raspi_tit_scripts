# raspi_tit_scripts
repo for aviary raspi scripts and tests


For installation on Pis:
run  ```python3 fresh_install_pi.py``` from the tower
OR
SSH into pi
clone repo to home directory
set chmod +x for files in "launchers" directory
After either option, add the following to crontab:
```bash
@reboot sh /home/pi/raspi_tit_scripts/launchers/CORRECTVERSION_launcher.sh 2 >> /home/pi/raspi_tit_scripts/tower_scripts/errorlog
```
reboot and profit

for installation on tower, add the following to crontab:
```
00 07 * * * ~/raspi_tit_scripts/launchers/check_ok_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
00 10 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
00 15 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
00 20 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh 2 >> ~/raspi_tit_scripts/tower_scripts/errorlog
```

To monitor live puzzles, ssh into pi and run ```tail -F <path to repo>/logs```. the python programs are run by launchers with -u flag to leave stdout unbuffered. Use tmux to keep everything in one place.

Make sure that the List_of_Cameras is kept up to date with pi name, IP address
Also double-check the mount points for the server

