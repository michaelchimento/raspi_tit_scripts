#!/bin/sh
# feederlauncher.sh
# launches correct python scripts with directory management

cd /home/pi/raspi_tit_scripts
sleep 10
python3 feeder_photos.py&
exit 0