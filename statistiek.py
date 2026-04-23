#!/bin/python3

import json, datetime

dbfile = "db.json"
statef = "crawler/state.json"

nu = datetime.datetime.now().date()

with open(dbfile) as f:
	db = json.load(f)

ras = {}

for i in db["schaap"]:
	schaap = db["schaap"][i]
	try:
		r = schaap["Ras"]
		if not r in ras:	ras[r] = {'leeft':0, 'totaal':0, 'ram':0, 'ooi':0, 'lam':0, 'Nu bij':[],'worpen':0,'lammen':0}
		ras[r]['totaal'] = ras[r]['totaal'] + 1
		#if "Aantal worpen" in schaap and "Aantal lammeren" in schaap and "Geslacht" in schaap:
		#	if schaap["Geslacht"] == "V": # Worpen gelden aan beide kanten van de geslachtskloof.
		#		ras[r]['worpen'] = ras[r]['worpen'] + schaap["Aantal worpen"]
		#		ras[r]['lammen'] = ras[r]['lammen'] + schaap["Aantal lammeren"]
		if "leeft" in schaap and schaap["leeft"]:
			ras[r]['leeft'] = ras[r]['leeft'] + 1
			if schaap["nu bij"] not in ras[r]["Nu bij"]:
				ras[r]["Nu bij"].append(schaap["nu bij"])
			geboren = datetime.datetime.strptime(schaap["Gebdat"], '%d/%m/%Y').date()
			leeftijd = nu - geboren
			if leeftijd.days <= 300:
				ras[r]['lam'] = ras[r]['lam'] + 1
			else:
				if schaap['Geslacht'] == 'V':
					ras[r]['ooi'] = ras[r]['ooi'] + 1
				if schaap['Geslacht'] == 'M':
					ras[r]['ram'] = ras[r]['ram'] + 1
	except KeyError:
		pass

smax = None
omax = None
for s in db['schaap']:
	schaap = db['schaap'][s]
	if "kind" in schaap and "Geslacht" in schaap:
		if schaap["Geslacht"] == "M":
			if smax == None or len( schaap["kind"] ) > len( smax["kind"] ):
				smax = schaap
		if schaap["Geslacht"] == "V":
			if omax == None or len( schaap["kind"] ) > len( omax["kind"] ):
				omax = schaap
				if not "Naam" in omax:	omax["Naam"] = omax["VNLid"]

if smax != None: print("Meest productieve ram is {}, een {} met {} kinderen.".format(smax["Naam"], smax["Ras"], len( smax["kind"] ) ) )
if omax != None:print("Meest productieve ooi is {}, een {} met {} kinderen.".format(omax["Naam"], omax["Ras"], len( omax["kind"] ) ) )

smax = None
gmax = None
for f in db['fokker']:
	fokker = db['fokker'][f]
	if 'stal' in fokker:
		if smax == None or len( fokker['stal'] ) > len( db['fokker'][smax]['stal'] ):
			smax = f
	if 'geboren' in fokker:
		if gmax == None or len( fokker['geboren'] ) > len( db['fokker'][gmax]['geboren'] ):
			gmax = f

if smax != None: print("Fokker met de meeste dieren ({}) is {}.".format( len( db['fokker'][smax]['stal']), smax ) )
if gmax != None: print("Meest productieve fokker ({} geboortes) is {}.".format( len( db['fokker'][gmax]['geboren']), gmax ) )

#keys = sorted( list(gtd.keys()) )
#print("Genotypes in het stamboek:")
#for k in keys:
#	print("{:<16} {}".format(k, gtd[k]))

d = 0
for r in ras:
	d = d + ras[r]['leeft']

print("Fokkers hebben gemiddeld {:.3f} schapen.".format( d / len(db["fokker"])))
print("Database bevat nu {} schapen en {} fokkers.".format(len(db["schaap"]), len(db["fokker"])))
print(    "Ras                         Levend Ooi  Ram  Lam  Totaal Eigenaars nr/eigenaar")# worpindex")
for r in sorted( list(ras.keys()) ):
	s = "{:<27} {:<6} {:<4} {:<4} {:<4} {:<6} {:<9} ".format(r, ras[r]['leeft'], ras[r]['ooi'], ras[r]['ram'], ras[r]['lam'], ras[r]['totaal'], len(ras[r]["Nu bij"]))
	if len(ras[r]["Nu bij"]) > 0:
		s = s + "{:<5.1f}       ".format( ras[r]['leeft'] / len(ras[r]["Nu bij"]) )
	else:
		s = s + "            "
	#if ras[r]["worpen"] > 0:
	#	s = s + "{:<5.3f}".format(ras[r]['lammen'] / ras[r]["worpen"] )
	#else:
	#	s = s + "     "
	print(s)














	
































