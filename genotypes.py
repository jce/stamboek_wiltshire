#!/bin/python3
import json, datetime

nu = datetime.datetime.now().date()

with open("db.json") as f:
	db = json.load(f)

gtd = {}

for i in db["schaap"]:
	schaap = db["schaap"][i]
	try:
		gt = schaap["Genotype"]
		if not gt in gtd:
			gtd[gt] = 0
		gtd[gt] = gtd[gt] +1
	except KeyError:
		pass	

# Sorted by value
# https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
gtd = {k: v for k, v in sorted(gtd.items(), key=lambda item: item[1], reverse=True)}
print("Genotypes in het stamboek:")
for k in gtd:
	print("{:<10} {}".format(k, gtd[k]))













	
































