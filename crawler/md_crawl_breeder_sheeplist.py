#!/bin/python3

# Stage 2 script for the scraper. Should run only once to completion. 
# If fails, restart from stage 1.

import json
from bs4 import BeautifulSoup as bs
import requests, time, random, datetime
from login import *

session = requests.session()
dbfile = "../db.json"
statef = "state.json"
URL = "https://vnl.falcooonline.com/VNLonline/FrmZoekDieren2.aspx?E="

with open(statef) as f:
	state = json.load(f)
if not "todo" in state: state["todo"] = []
if not "done" in state: state["done"] = []
if state["first_2"]:
	state["leeft"] = [] # This script decides who lives.
	state["first_2"] = False
	
try:
	with open(dbfile) as f:
		db = json.load(f)
except FileNotFoundError:
	db = {}
if not "fokker" in db: db["fokker"] = {}
if not "schaap" in db: db["schaap"] = {}

# Store database and state
def store():
	with open(dbfile, 'w', encoding='utf-8') as f:
		json.dump(db, f, sort_keys=True, ensure_ascii=False, indent=2)
	with open(statef, 'w', encoding='utf-8') as f:
		json.dump(state, f, sort_keys=True, ensure_ascii=False, indent=2)

# Read breeder sheeplist from given website id.
def lees_fokker_stallijst(id):
	id = str(id)

	page = session.get(URL + str(id))
	s = bs(page.text, 'html5lib')

	if page.text.find("Gebruikersnaam") > 0 and page.text.find("Paswoord") > 0:
		login(session, s)
		page = session.get(URL + str(id))
		s = bs(page.text, 'html5lib')

	fokker = s.find(id="LabInfo").text
	db["fokker"][fokker] = state["fokker_op_id"][id]
	del state["fokker_op_id"][str(id)]
	
	row = s.find(id="DataGrid1").tbody.find_all('tr')
	schapen = []
	for i in range(1, len(row)):
		field = row[i].find_all('td')
		VNLid = field[0].text
		id = str(field[0].a).replace('?', '\"').split('\"')[2]

		# Sheep belongs now to th is breeder.
		if not "stal" in db["fokker"][fokker]:
			db["fokker"][fokker]["stal"] = []
		if not id in db["fokker"][fokker]["stal"]:
			db["fokker"][fokker]["stal"].append(id)

		# Sheep ends up in sheep list.
		db["schaap"][id] = {}
		db["schaap"][id]["VNLid"] = VNLid
		db["schaap"][id]["leeft"] = True
		db["schaap"][id]["laatst levend gezien"] = datetime.datetime.now().strftime("%d/%m/%Y")
		if not "toen bij" in db["schaap"][id]:
			db["schaap"][id]["toen bij"] = {}
		db["schaap"][id]["toen bij"][datetime.datetime.now().strftime("%d/%m/%Y")] = fokker
		db["schaap"][id]["nu bij"] = fokker
		
		# Sheep goes to the todo list, and gets removed from the done
		# list. Any alive sheep can be new or have changed properties,
		# so they need to be refetched.
		if not id in state["todo"]:
			state["todo"].append(id)
			if id in state["done"]:
				state["done"].remove(id)

		# Append to alive list
		state["leeft"].append(id)
		
		# Append to sheep list for console display
		schapen.append(VNLid)
		
	# Display to console
	print("{} sheeplist: {} sheep".format(fokker, len(schapen)));

for fokker_id in list( state["fokker_op_id"].keys() ):
	lees_fokker_stallijst(fokker_id)
	store()
	time.sleep(random.random() * 4 + 2)	

# All sheep who were already alive have to be re-fetched as well. Some
# may have died in the meantime (no longer on any breeder's sheeplist).
for schaap_id in db["schaap"]:
	if "leeft" in db["schaap"][schaap_id] and db["schaap"][schaap_id]["leeft"]:
		if schaap_id not in state["todo"]:
			state["todo"].append(schaap_id)
			if id in state["done"]:
				state["done"].remove(schaap_id)
        
store()































