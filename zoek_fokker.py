#!/bin/python3

import datetime, json, sys


def main():
	with open("db.json") as f:
		db = json.load(f)

	search = sys.argv[1]

	rv = zoek_fokkers(db, search)

	print(json.dumps(rv, indent=2))

# Voor intern gebruik
zoek_waar = ["naam", "UBN", "VNLid", "adres", "email", "telefoonnr", "woonplaats"]
def zoek_2(f, wie, waar, wat, rv):
    # f = inhoud van deze ene fokker
    # wie = naam van deze ene fokker (sleutel in db.json)
    # waar = member field waar te kijken
    # wat = String waar de gebruiker op wil zoeken
    # rv = dict met gevonden fokkers
	try:
		if str(f[waar]).find(wat) != -1 and not wie in rv:
			rv[wie] = f
	except KeyError:
		pass
	if waar == "naam":
		if wie.find(wat) != -1 and not wie in rv:
			rv[wie] = f

# Vindt fokkers terug, gegeven een (deel van de) string in een zoeklocatie. 
# db: stamboek database
# s: unieke string waarop te zoeken
# rv: tabel fokkers die voldoen aan de zoekstring
def zoek_fokkers(db, search):
	rv = {}
	for i in db["fokker"]:
		f = db["fokker"][i]
		for w in zoek_waar:
			zoek_2(f, i, w, search, rv)
	return rv

if __name__ == "__main__":
	main()
