#!/bin/sh
# puzzlelauncher.sh
# launches correct python scripts with directory management

cd /home/pi/raspi_tit_scripts
python3 puzzle_video.py&
python3 rfid_code.py&
exit 0
