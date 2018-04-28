import csv

with open('all_abstracts.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter = ',')
	for row in reader:
		print (row[1])
