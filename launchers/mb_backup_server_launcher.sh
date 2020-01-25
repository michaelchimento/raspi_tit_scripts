#!/bin/sh
# backup_server_launcher.sh
# launches correct python scripts with directory management

cd ~/raspi_tit_scripts/tower_scripts
sleep 10
python3 mb_backup_function.py&
exit 0
