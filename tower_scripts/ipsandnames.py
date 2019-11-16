#!/usr/bin/python3

import csv
import socket

with open('../List_of_Cameras.csv') as csvfile:
	data = csv.reader(csvfile, delimiter=',', escapechar="#")
	pi_data_table = [row for row in data]
