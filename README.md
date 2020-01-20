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
@reboot sh /home/pi/raspi_tit_scripts/launchers/CORRECTVERSION_launcher.sh >/home/pi/raspi_tit_scripts/logs 2>&1
```
reboot and profit

for installation on tower, add the following to crontab:
```
55 06 * * * ~/raspi_tit_scripts/launchers/check_ok_launcher.sh >> ~/raspi_tit_scripts/logs 2>&1
00 11 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh >> ~/raspi_tit_scripts/logs 2>&1
30 17 * * * ~/raspi_tit_scripts/launchers/download_video_launcher.sh >> ~/raspi_tit_scripts/logs 2>&1
00 01 * * * ~/raspi_tit_scripts/launchers/backup_server_launcher.sh >> ~/raspi_tit_scripts/logs 2>&1
```

Nothing really to note, except make sure that the List_of_Cameras is kept up to date with pi name, IP address
Also double-check the mount points for the server

