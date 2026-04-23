#!/bin/python3

import json
from bs4 import BeautifulSoup as bs
import requests, time, random, signal, sys, datetime
from login import *

dbfile = "../db.json"
statef = "state.json"
URL = "https://vnl.falcooonline.com/VNLonline/FrmStamboomDier2.aspx?"
ras_of_interest = [] #["none"] #["Wiltshire Horn"]
run = True

# Allow for breaking with Ctrl+C (or SystemD)
def signal_handler(sig, frame):
	print("signal received. Bye")
	global run
	run = False
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

with open(dbfile) as f:
	db = json.load(f)
with open(statef) as f:
    state = json.load(f)

session = requests.Session()

def tag(sheep_id, d1, tag):
	# Search data for tag: smthing<br....
	#                xxxxxx-------xxxxxx
	# smthing then goes in db under the schaap[tag] as string or int
	try:
		start = d1.index(tag)
		end = d1.index("<", start)
		val = d1[start+len(tag)+2:end].strip()
		if len(val) > 0:
			try:
				val = int(val)
			except ValueError:
				pass
			# Drop 0, empty and '.'.
			if val != 0 and val != "." and val != "":
				print("{}: {}".format(tag, val))
				db["schaap"][sheep_id][tag] = val
	except ValueError:
		pass 

def lees_schaap(sheep_id):
    sheep_id = str(sheep_id)

    havepage = False
	
    while not havepage:
        try:
            page = session.get(URL + str(sheep_id))
            s = bs(page.text, 'html5lib')
		
            if page.text.find("Gebruikersnaam") > 0 and page.text.find("Paswoord") > 0:
                login(session, s)	
            else:
                havepage = True
        except requests.exceptions.ConnectionError:
            print("!!!!!!!!!!!!!!!!! CONNECTION ERROR, retrying in ~ 30 seconds !!!!!!!!!!!!!!!!!!!!!!!")
            time.sleep(random.random() * 20 + 20)	

    d1 = str(s.find(id="d1"))
    print("------------------------------------------------")
    VNLid = s.find(id="d1").a.text
    db["schaap"][sheep_id]["VNLid"] = VNLid
    print("Stamboek nr: {}".format(VNLid))
    print("id: {}".format(sheep_id))
    tag(sheep_id, d1, "Naam")
    tag(sheep_id, d1, "LevensNr")
    tag(sheep_id, d1, "WerkNrLNV")
    tag(sheep_id, d1, "Gebdat")
    tag(sheep_id, d1, "Geslacht")
    tag(sheep_id, d1, "Status")
    tag(sheep_id, d1, "Worpgrootte")
    tag(sheep_id, d1, "Vader")
    tag(sheep_id, d1, "Moeder")
    tag(sheep_id, d1, "Aantal worpen")
    tag(sheep_id, d1, "Aantal lammeren")
    tag(sheep_id, d1, "Genotype")
    tag(sheep_id, d1, "Stamboekwaardig")
    tag(sheep_id, d1, "Bijzonderheden")
    tag(sheep_id, d1, "Kleur")
    tag(sheep_id, d1, "Hoofd")
    tag(sheep_id, d1, "Horens")
    tag(sheep_id, d1, "Nek / Hals")
    tag(sheep_id, d1, "Voorhand")
    tag(sheep_id, d1, "Middenhand")
    tag(sheep_id, d1, "Achterhand")
    tag(sheep_id, d1, "Beenwerk")
    tag(sheep_id, d1, "Staart")
    tag(sheep_id, d1, "Aftekening / Vacht")
    tag(sheep_id, d1, "Ras")
    tag(sheep_id, d1, "Fokker")

    if sheep_id in state["leeft"]:
        print("Nu bij: {}".format(db["schaap"][sheep_id]["nu bij"]))
        db["schaap"][sheep_id]["leeft"] = True
    else: # Not in leeft list. sheep_id is added to leeft with fetching of breeder sheeplists.
        if "leeft" in db["schaap"][sheep_id] and db["schaap"][sheep_id]["leeft"]:
            db["schaap"][sheep_id]["eerst niet levend"] = datetime.datetime.now().strftime("%d/%m/%Y")
        db["schaap"][sheep_id]["leeft"] = False

    if "Fokker" in db["schaap"][sheep_id]:
        fokker = db["schaap"][sheep_id]["Fokker"]
        if not fokker in db["fokker"]:
            db["fokker"][fokker] = {}
        if not "geboren" in db["fokker"][fokker]:
            db["fokker"][fokker]["geboren"] = []
        if id not in db["fokker"][fokker]["geboren"]:
            db["fokker"][fokker]["geboren"].append(sheep_id)

    try:
        wg = db["schaap"][sheep_id]["Worpgrootte"]
        wg = str().join(filter(str.isdigit, wg))
        db["schaap"][sheep_id]["Worpgrootte"] = int(wg)
    except ValueError:
        del db["schaap"][sheep_id]["Worpgrootte"]
    except KeyError:
        pass
			
    # Search the page for parents, add to db
    ouders = []
    td = s.find(id="TabStam").find_all("td")
    for i in range(2, 16):

        oVNLid = td[i].a.text

        oid =  str(td[i].a).replace('?', '\"').split('\"')[2] 
        if oid == "0" or oid == "": continue
        ouders.append(oVNLid)

        if i == 2:
            db["schaap"][sheep_id]["vader_id"] = oid
        if i == 9:
            db["schaap"][sheep_id]["moeder_id"] = oid

        if not oid in db["schaap"]: db["schaap"][oid] = {}
        db["schaap"][oid]["VNLid"] = oVNLid

        if ( len(ras_of_interest) == 0 or ("Ras" in db["schaap"][sheep_id] and db["schaap"][sheep_id]["Ras"] in ras_of_interest)) and oid not in state["todo"] and oid not in state["done"]:
            state["todo"].append(oid)

    if len(ouders) > 0: 
        print("Ouders (3 gen): {}".format(ouders))

	# Search the page for children, add to db
    kinderen = []
    for child in s.find(id="TabNakomelingen").tbody.children:
		# Not all children fields represent nakomelingen
        try:

            cVNLid = child.a.text

            kinderen.append(cVNLid)
            cid = str(child.a).replace('?', '\"').split('\"')[2] 

            if not cid in db["schaap"]: db["schaap"][cid] = {}
            db["schaap"][cid]["VNLid"] = cVNLid

            if not "kind" in db["schaap"][sheep_id]: db["schaap"][sheep_id]["kind"] = []
            if not cid in db["schaap"][sheep_id]["kind"]:
                db["schaap"][sheep_id]["kind"].append(cid)

                if (len(ras_of_interest) == 0 or ("Ras" in db["schaap"][sheep_id] and db["schaap"][sheep_id]["Ras"] in ras_of_interest)) and cid not in state["todo"] and cid not in state["done"]:
                    state["todo"].append(cid)

        except AttributeError:
            pass

    if len(kinderen) > 0: print("Kinderen: {}".format(kinderen))
    if not sheep_id in state["done"]:
        state["done"].append(sheep_id)

def store_db():
    print("XXXXXXXXXXXXXXXXX   Storing DB  XXXXXXXXXXXXXXXXX")
    with open(dbfile, 'w', encoding='utf-8') as f:
        json.dump(db, f, sort_keys=True, ensure_ascii=False, indent=2)
    with open(statef, 'w', encoding='utf-8') as f:
        json.dump(state, f, sort_keys=True, ensure_ascii=False, indent=2)
    print("XXXXXXXXXXXXXXXXXXXX   Done  XXXXXXXXXXXXXXXXXXXX")

def now():
	return datetime.datetime.timestamp(datetime.datetime.now())

sc = 0
last = now()
next = now()
while len(state["todo"]) > 0 and run:

	time_to_next = next - now()
	if time_to_next <= 0:

		sheep_id = state["todo"].pop(0)
		lees_schaap(sheep_id)
		sc = sc + 1
		if sc >= 100:
			store_db()
			sc = 0
		next = now() + 2 + random.random() * 4

	if time_to_next > 0 and time_to_next <= 0.5:
		time.sleep(time_to_next)

	if time_to_next > 0.5:
		time.sleep(0.5)	

store_db()


