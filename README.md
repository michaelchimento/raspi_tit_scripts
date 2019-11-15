# raspi_tit_scripts
repo for aviary raspi scripts and tests


For installation on Pis:
SSH into pi
clone repo to home directory
set chmod +x for files in "launchers" directory

run crontab and add:
@reboot sh /home/pi/raspi_tit_scripts/launchers/CORRECTVERSION_launcher.sh >/home/pi/raspi_tit_scripts/logs 2>&1

reboot and profit

For installation on main towers:
Nothing really to note, except make sure that the List_of_Cameras is kept up to date with pi name, IP address (no need for @pi)
Add crontab jobs to download videos

