#!/bin/sh
# puzzlelauncher.sh
# launches correct python scripts with directory management


cd /home/pi/raspi_tit_scripts
sleep 10
python3 -u upload_to_server2020.py > logs/upload_logs&
exit 0
