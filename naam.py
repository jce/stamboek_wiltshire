#!/bin/python3

#Mode determined by script name (symlink: naamooi.py / naamram.py)

import json, string, sys

with open("db.json") as f:
	db = json.load(f)

mode = "all"    # Mode of operation, all names, or ewe names or ram names.
if "ooi" in sys.argv[0]:
    mode = "ooi"
if "ram" in sys.argv[0]:
    mode = "ram"

namen = {}

for schaap in db["schaap"].values():
    naam = schaap.get("Naam")
    if not isinstance(naam, str):
        continue    
    
    geslacht = schaap.get("Geslacht")

    if not (
        mode == "all" or
        (mode == "ooi" and geslacht == "V") or
        (mode == "ram" and geslacht == "M")
    ):
        continue

    parts = naam.replace('-', ' ').split()
    if not parts:
        continue

    for n in parts:
        #n = n.strip(string.punctuation)
    
        if any(c in string.punctuation for c in n):
            continue
               
        if not n.isalpha():
            continue

        if len(n) <= 2:
            continue

        namen[n] = namen.get(n, 0) + 1

namen_c = sorted(namen.items(), key=lambda x: x[1], reverse=True)
for n, c in namen_c:
    print("{:20} {}".format(n, c))












	
































