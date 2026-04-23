#!/bin/python3

import json, datetime

nu = datetime.datetime.now().date()

with open("db.json") as f:
	db = json.load(f)

# Geeft een worpen per jaar en maand tabel voor een lijst rassen.
def worpindex(ras=[]):
	
	# worp structuur:
	# jaar(int) - maand(int) - worp(int) en aantal(int)
	wi = {}
	# Worpenlijst, voorkomt doublures
	# schaap id(str) - worpdatum(str)
	w = {}
	for i in db["schaap"]:
		schaap = db["schaap"][i]
		try:
			moeder = schaap["moeder_id"]
			if not moeder in w: w[moeder] = []
			r = schaap["Ras"]
			if r in ras or len(ras) == 0:
				Gebdat = schaap["Gebdat"]
				if not Gebdat in w[moeder]:
					geboren = datetime.datetime.strptime(Gebdat, '%d/%m/%Y').date()
					y = geboren.year
					m = geboren.month
					l = int(schaap["Worpgrootte"])
					w[moeder].append(Gebdat)
					if not y in wi:	wi[y] = {}
					if not m in wi[y]:	wi[y][m] = {"worpen":0, "lammen":0}
					wi[y][m]["worpen"] = wi[y][m]["worpen"] + 1
					wi[y][m]["lammen"] = wi[y][m]["lammen"] + l
		except KeyError:
			pass

	for y in wi:
		for m in wi[y]:
			wi[y][m]["index"] = wi[y][m]["lammen"] / wi[y][m]["worpen"]

	return wi


#wi = worpindex(["Wiltshire Horn"])
wi = worpindex()
gmin = 25

jaren = sorted(wi)
start = jaren[0]
eind = jaren[-1]

print("worpindex per jaar en maand, minimum {} worpen per tijdvak".format(gmin))
print("jaar jan  feb  mar  apr  mei  jun  jul  aug  sep  oct  nov  dec  tot")
for j in range(start, eind+1):
	l = str(j) + " "
	w = 0
	g = 0
	if not j in wi:
		print(l)
		continue
	for m in range(1, 13):
		if m in wi[j] and wi[j][m]["worpen"] >= gmin:
			l = l + "{:<1.2f} ".format(wi[j][m]["index"])
			w = w + wi[j][m]["worpen"]
			g = g + wi[j][m]["lammen"]
		else:
			l = l + "     "
	if w >= gmin:
		l = l + "{:<1.2f}".format(g/w)
	print(l)






