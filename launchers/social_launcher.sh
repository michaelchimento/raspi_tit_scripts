#!/bin/sh
# sociallauncher.sh
# launches correct python scripts with directory management

cd /home/pi/raspi_tit_scripts
sleep 15
python3 social_photos.py >> logs/logs&
exit 0
