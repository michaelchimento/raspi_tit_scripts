import csv

with open('List_of_Cameras.csv') as csvfile:
	data = csv.reader(csvfile, delimiter=',')
	pi_data_table = [row for row in data]
