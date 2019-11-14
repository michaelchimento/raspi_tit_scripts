#!/usr/bin/python3

import csv
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

with open('List_of_Cameras.csv') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    pi_data_table = [row for row in data]
pi_dict = dict(pi_data_table)

#get ip_address and cross reference in dictionary
ipaddress = get_ip()
name = [key  for (key, value) in pi_dict.items() if value == pi_IP][0]



###############    ###############
#Puzzle_P1_C1      #Puzzle_Px_C2
#                  #
#Social_P1_C1      #Social_Px_C2
#                  #
#Observ_P1_C1      #Observ_Px_C2
#                  #
#Feeder_P1_C1      #Feeder_Px_C2
#                  #
#Wormpt_P1_C1      #Wormpt_Px_C2
#                  #
###############    ###############
###############    ###############
#Puzzle_P2_C3      #Puzzle_Px_C4
#                  #
#Social_P2_C3      #Social_Px_C4
#                  #
#Observ_P2_C3      #Observ_Px_C4
#                  #
#Feeder_P2_C3      #Feeder_Px_C4
#                  #
#Wormpt_P2_C3      #Wormpt_Px_C4
#                  #
###############    ###############
###############    ###############
#Puzzle_P3_C5      #Puzzle_Px_C6
#                  #
#Social_P3_C5      #Social_Px_C6
#                  #
#Observ_P3_C5      #Observ_Px_C6
#                  #
#Feeder_P3_C5      #Feeder_Px_C6
#                  #
#Wormpt_P3_C5      #Wormpt_Px_C6
#                  #
###############    ###############
###############    ###############
#Puzzle_P4_C7      #Puzzle_Px_C8
#                  #
#Social_P4_C7      #Social_Px_C8
#                  #
#Observ_P4_C7      #Observ_Px_C8
#                  #
#Feeder_P4_C7      #Feeder_Px_C8
#                  #
#Wormpt_P4_C7      #Wormpt_Px_C8
#                  #
###############    ###############
###############    ###############
#Puzzle_P5_C9      #Puzzle_Px_C10
#                  #
#Social_P5_C9      #Social_Px_C10
#                  #
#Observ_P5_C9      #Observ_Px_C10
#                  #
#Feeder_P5_C9      #Feeder_Px_C10
#                  #
#Wormpt_P5_C9      #Wormpt_Px_C10
#                  #
###############    ###############






name = "Wormpt_P5_C9"
ipaddress = "10.76.0.115"
