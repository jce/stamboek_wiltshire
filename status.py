#!/bin/python3
ras = "Wiltshire Horn"
import json, datetime

nu = datetime.datetime.now().date()

with open("db.json") as f:
	db = json.load(f)

std = {}

for i in db["schaap"]:
    schaap = db["schaap"][i]
    try:
        if ras == "" or schaap["Ras"] == ras:
            st = schaap["Status"]
            if not st in std:
                std[st] = 0
            std[st] = std[st] +1
    except KeyError:
        pass	

# Sorted by value
# https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
std = {s: v for s, v in sorted(std.items(), key=lambda item: item[1], reverse=True)}
print("Status in het stamboek:")
for s in std:
	print("{:<10} {}".format(s, std[s]))













	
































