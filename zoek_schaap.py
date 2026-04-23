#!/bin/python3

import datetime, json, sys


def main():
	with open("db.json") as f:
		db = json.load(f)

	search = sys.argv[1]

	rv = zoek_schapen(db, search)

	print(json.dumps(rv, indent=2))

# Voor intern gebruik
zoek_waar = ["Naam", "LevensNr", "VNLid", "id"]
#zoek_waar = ["Naam", "LevensNr", "VNLid", "id", "nu bij"]
def zoek_2(s, wie, waar, wat, rv):
	# Veel onduidelijker kon ik niet zijn toch? XD
	# JCE, 3-5-2024
	try:
		if str(s[waar]).find(wat) != -1 and not wie in rv:
			rv[wie] = s
	except KeyError:
		pass
	if waar == "id":
		if wie.find(wat) != -1 and not wie in rv:
			rv[wie] = s

# Vindt schapen terug, gegeven een (deel van de) string in een zoeklocatie. 
# db: stamboek database
# s: unieke string waarop te zoeken
# rv: tabel schapen die voldoen aan de zoekstring
def zoek_schapen(db, search):
	rv = {}
	for i in db["schaap"]:
		s = db["schaap"][i]
		for w in zoek_waar:
			zoek_2(s, i, w, search, rv)
	return rv

# Zoekt een schaap, gegeven een deel van de string in een zoeklocatie.
# Bij vinden van meerdere schapen: FOUT!
# Geeft de inhoud van het schaap object. het id is toegevoegd aan de inhoud.
def zoek_schaap(db, search):
	s = zoek_schapen(db, search)
	assert(len(s) == 1)
	rv = {}
	for id in s:
		for item in s[id]:
			rv[item] = s[id][item]
		rv["id"] = id
	return rv

if __name__ == "__main__":
	main()
