#!/bin/python3

output_csv = True
gmin = 25
jmax = 10

import json, datetime

dbfile = "db.json"

nu = datetime.datetime.now().date()

with open(dbfile) as f:
	db = json.load(f)

# Doel: per ras een worpindex voor 1e jaar, 2+e jaar

def worpindex():
	
	# worp structuur:
	# ras - kalenderjaar sinds geboorte (dus geen dt in jaar) - worp en aantal (int en int)
	wi = {}						# wi -> worpindex
	# Worpenlijst, voorkomt doublures
	# schaap id(str) - worpdatum(str)
	w = {}						# w -> worplijst
	for i in db["schaap"]:		# index
		schaap = db["schaap"][i]
		try:
			moeder = schaap["vader_id"]
			ras = schaap["Ras"]
			Gebdat = schaap["Gebdat"]

			if not moeder in w: w[moeder] = []
			if not Gebdat in w[moeder]:
				w[moeder].append(Gebdat)

				geboren = datetime.datetime.strptime(Gebdat, '%d/%m/%Y').date()
				mgeboren = datetime.datetime.strptime(db["schaap"][moeder]["Gebdat"], '%d/%m/%Y').date()
				mleeftijd = geboren.year - mgeboren.year
				worpgrootte = int(schaap["Worpgrootte"])
				if not ras in wi:	wi[ras] = {}
				if not mleeftijd in wi[ras]: wi[ras][mleeftijd] = {"worpen":0, "lammen":0}
				wi[ras][mleeftijd]["worpen"] = wi[ras][mleeftijd]["worpen"] + 1
				wi[ras][mleeftijd]["lammen"] = wi[ras][mleeftijd]["lammen"] + worpgrootte
		except KeyError:
			pass

	for ras in wi:
		for mleeftijd in wi[ras]:
			wi[ras][mleeftijd]["index"] = wi[ras][mleeftijd]["lammen"] / wi[ras][mleeftijd]["worpen"]

	return wi

wi = worpindex()

print("worpindex per ras op leeftijd, minimaal {} worpen per leeftijdsvak.".format(gmin))
l = "ras               jaar "
for j in range(jmax+1): 
	l = l + "    {:<2}".format(j)
print(l)
for r in sorted(wi):
	l = "{:<26}".format(r)
	any=False
	for j in range(0, jmax+1):
		if j in wi[r] and wi[r][j]["worpen"] >= gmin:
			l = l + " {:5.3f}".format(wi[r][j]["index"])
			any=True
		else:
			l = l + "  .   " 
	if any:	print(l)

if output_csv:
	print("Writing worpindex2.csv")
	f = open("worpindex2.csv", "w")
	f.write("worpindex per ras op leeftijd, minimaal {} worpen per leeftijdsvak.\n".format(gmin))                                                                                                                                                                     
	f.write("ras;jaar")                                                                                                                                                                                                                                 
	for j in range(0, jmax+1): 
		f.write(";{:<2}".format(j))
	f.write("\n")                                                                                                                                                                                                                                 
	for r in sorted(wi):
		any=False 
		line = ""
		for j in range(0, jmax+1):
			if j in wi[r] and wi[r][j]["worpen"] >= gmin: 
				line = line + "{:5.3f};".format(wi[r][j]["index"])
				any=True
			else:
				line = line + ";" 
		if any:
			f.write("{};".format(r) + ";" + line + "\n")
