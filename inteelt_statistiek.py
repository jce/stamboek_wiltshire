#!/bin/python3

import json, datetime

dbfile = "db.json"

nu = datetime.datetime.now().date()

with open(dbfile) as f:
	db = json.load(f)

minst_inteelt = db["schaap"][next(iter(db["schaap"]))]
meest_inteelt = minst_inteelt
 
aantal = {}
som = {}

for i in db["schaap"]:
	s = db["schaap"][i]
	try:
		if s["Ras"] == "Wiltshire Horn" and s["Status"] == "V":
			if s["inteelt"] < minst_inteelt["inteelt"]:
				minst_inteelt = s
			if s["inteelt"] > meest_inteelt["inteelt"]:
				meest_inteelt = s
			geboren = datetime.datetime.strptime(s["Gebdat"], '%d/%m/%Y').date()
			geboortejaar = geboren.year
			if not geboortejaar in aantal:
				aantal[geboortejaar] = 0
				som[geboortejaar] = 0
			aantal[geboortejaar] = aantal[geboortejaar] + 1
			som[geboortejaar] = som[geboortejaar] + s["inteelt"]
				
	except KeyError:
		pass	

print("Het Wiltshire Horn schaap met meeste inteelt is:")
print(meest_inteelt)

print("jaar	gemiddeld inteelt")
for i in sorted(aantal):
	if aantal[i] >= 50:
		print("{}	{}".format(i, som[i]/aantal[i]))


	
































