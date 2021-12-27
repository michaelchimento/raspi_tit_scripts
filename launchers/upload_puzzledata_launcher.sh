#!/bin/sh
# puzzlelauncher.sh
# launches correct python scripts with directory management


cd /home/michael/raspi_tit_scripts/tower_scripts
sleep 10
python3 -u download_puzzle_data.py > ../logs/download_puzzle_logs&
exit 0
