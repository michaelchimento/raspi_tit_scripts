#!/bin/sh
# puzzlelauncher.sh
# launches correct python scripts with directory management


cd /home/pi/raspi_tit_scripts
sleep 15
python3 -u  puzzle_video.py >> logs/video_logs&
python3 -u rfid_code_2021.py >> logs/logs&
exit 0
