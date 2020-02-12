#!/bin/sh
# download_video_launcher.sh
# launches correct python scripts with directory management

cd ~/raspi_tit_scripts/tower_scripts
sleep 10
python3 -u dl_video_from_pi_to_tower.py >> logs_video_dl 2>&1 &
exit 0
