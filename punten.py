#!/bin/python3

ras = "Wiltshire Horn"

import json

with open("db.json") as f:
	db = json.load(f)

# table[property][score] = occurrance
tab = {}
def register_property(pname, pvalue):
    if not pname in tab:
        tab[pname] = {}
    if not pvalue in tab[pname]:
        tab[pname][pvalue] = 0
    tab[pname][pvalue] = tab[pname][pvalue] + 1

properties = ["Hoofd", "Horens", "Nek / Hals", "Voorhand", "Middenhand", "Achterhand", "Beenwerk", "Staart", "Aftekening / Vacht"]

for i in db["schaap"]:
    s = db["schaap"][i]
    try:
        if ras == "" or s["Ras"] == ras:
            for p in properties:
                try:
                    register_property(p, s[p])
                except KeyError:
                    pass
    except KeyError:
        pass

# We need an list of scores that are present
present_scores = []
for p in tab:
    for s in tab[p]:
        if s not in present_scores:
            present_scores.append(s)
present_scores = sorted(present_scores)

print("Hoevaak welke puntenwaarde is toegekend")
if ras != "":
    print("Ras: ", ras)

offset = 0
for p in tab:
    print("       ", end='')
    for x in range(offset):
        print(".    ", end="")
    print(p)
    offset = offset + 1

for s in present_scores:
    print("{:>3} ".format(s), end='')
    for p in tab:
        count = 0
        if s in tab[p]:
            count = tab[p][s]
        print("{:>4} ".format(count), end='')
    print("")


