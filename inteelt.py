#!/bin/python3

# Inteelt berekening, daar draaide heel deze onderneming om.
# https://en.wikipedia.org/wiki/Coefficient_of_inbreeding
# Inteelt coefficient = som van per gemeenschappelijke voorouder:
# 	0.5^(n-1) x ( 1 + Fa)
# n = aantal individuen in de lus
# Fa = Inteelt coefficient van de gemeenschappelijke voorouder
# De lus gaat niet meerdere keren door hetzelfde individu.
# Het individu zelf en de ouders tellen exact 1 keer mee.

# Leuk, volgensmij kan je ook een Fa van 0 aannemen en dan mag
# de lus wel meermaals door hetzelfde individu. Maakt het 
# algoritme veel simpeler.
# JCE, 23-4-2026: Nee dat mag niet, bij een route door eenzelfde
# individu wordt de verdringing niet meegenomen. Idealiter
# wordt het algoritme later vervangen door een meer correcte.

import json, datetime
fokker =    "FOKKER_NAAM_HIER"
ras =       "Wiltshire Horn"
agemax =    1  # jaar

def id_add(d,i,v):
	# In dictionary d, create item i if not exist, with value v
	# If it does exist, add v to it.
	# item i may also be a dict with item-values. v will be a
	# relative weight, multiplying the values.
	if isinstance(i, dict):
		for x in i:
			id_add(d, x, i[x] * v)
	else:
		if not i in d:
			d[i] = 0
		d[i] = d[i] + v

def ptree(db, s):
# Builds parent tree for sheep id s
# Returns: dict of parents and genetic contribution
# parent: 0.5, parent's parent: 0.25, parent's parent's parent 0.125 etc...
# Note that conribution sum is more than 1, the sum of each 
# known generation is 1.
	rv = {}
	id_add(rv, s, 1)
	if "moeder_id" in db["schaap"][s]:
		m = db["schaap"][s]["moeder_id"]
		rvm = ptree(db, m)
		id_add(rv, rvm, 0.5)
	if "vader_id" in db["schaap"][s]:
		v = db["schaap"][s]["vader_id"]
		rvv = ptree(db, v)
		id_add(rv, rvv, 0.5)
	return rv	

def bereken_inteelt_coefficient(db, id_ooi, id_ram):
	boom_ooi = ptree(db, id_ooi)
	boom_ram = ptree(db, id_ram)
	inteelt = 0
	for i in boom_ooi:
		if i in boom_ram:
			inteelt = inteelt + 0.5 * boom_ooi[i] * 0.5 * boom_ram[i]
	return inteelt

def main():
    
    with open("db.json") as f:
        db = json.load(f)
	
    # Individuen serie 1 en 2, hier ooi en ram genoemd.
    # Werkt met database ids.
    ooi = []
    for sid in db["fokker"][fokker]["stal"]:
        s = db["schaap"][sid]
        if s["Ras"] == ras and s["Geslacht"] == "V":
            ooi.append(sid)

    ram = []
    nu = datetime.datetime.now().date()
    for i in db["schaap"]:
        s = db["schaap"][i]
        try:
            if s["Ras"] == ras and s["Geslacht"] == "M" and s["leeft"]:
                if db["schaap"][s["vader_id"]]["Status"] == "V":
                    if db["schaap"][s["moeder_id"]]["Status"] == "V":
                        geboren = datetime.datetime.strptime(s["Gebdat"], '%d/%m/%Y').date()
                        leeftijd = nu - geboren
                        if leeftijd.days < agemax * 365:
                            ram.append(i)
        except KeyError:
            pass

    # Uitvoer tabel
    rv = []
    for r in range(len(ram)):
        row = [ db["schaap"][ram[r]]["VNLid"] ]
        sum = 0
        for o in range(len(ooi)):
            ic = bereken_inteelt_coefficient(db, ooi[o], ram[r])
            row.append( ic )
            sum = sum + ic
        row.append( sum / len(ooi) )
        row.append( db["schaap"][ram[r]]["nu bij"] )
        rv.append(row)

    # Sorteer op gemiddelde
    rv.sort(key=lambda x: x[len(ooi)+1])

    # Weergave
    print("Inteelt voor alle {} rammen die jonger zijn dan {} jaar, gekruist op al {}'s ooien.".format(ras, agemax, fokker))
    print("            ", end=""),
    for o in ooi:
        print("{:<11} ".format(db["schaap"][o]["VNLid"]), end="")
    print("gemiddeld  eigenaar")
    for r in range(len(ram)):
        print("{:<11} ".format(rv[r][0]), end="")
        for o in range(len(ooi)):
            print("  {:>7.3f} % ".format(rv[r][o+1] * 100), end="")
        print("{:>7.3f} % ".format(rv[r][o+2] * 100), end="")
        print(" " + rv[r][len(ooi)+2], end="")
        print("")

if __name__ == "__main__":
	main()










	
































