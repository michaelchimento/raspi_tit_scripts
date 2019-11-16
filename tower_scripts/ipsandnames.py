#!/usr/bin/python3

import csv
import socket

def decomment(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield raw

with open('tower_list_of_cameras.csv') as csvfile:
	data = csv.reader(decomment(csvfile), delimiter=',')
	pi_data_table = [row for row in data]
