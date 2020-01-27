#!/bin/sh
# puzzlelauncher.sh
# launches correct python scripts with directory management


cd /home/pi/raspi_tit_scripts
sleep 15
python3 puzzle_video.py&
python3 -u rfid_code.py > logs&
exit 0
