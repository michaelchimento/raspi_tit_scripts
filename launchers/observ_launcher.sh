#!/bin/sh
# observ_launcher.sh
# launches correct python scripts with directory management

cd /home/pi/raspi_tit_scripts
sleep 15
python3 observ_photos.py >> logs/logs&
exit 0
