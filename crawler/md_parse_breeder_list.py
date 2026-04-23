#!/bin/python3
import json
from bs4 import BeautifulSoup as bs
f = open("fokkerlijst.html", "rb")
s = bs(f.read(), 'html5lib')
dbfile = "../db.json"

try:
    with open("state.json") as f:
        state = json.load(f)
except:
    state = {}

fokker = {}
errors = 0

for child in s.body.table.tbody.children:   # or s.find(id="Datagrid1").tbody.children:
    try:
        td = child.findAll('td')
        id = str(td[0].a).replace('=', '\"').split('\"')[3]
        Naam = td[0].text
        # Okay, deze tabel doet achternaam - voornaam - tussenwoord. De rest doet voornaam - tussenwoord - achternaam
        # En no way om te herleiden wat bij elkaar hoorde, overal kunnen spaties in staan...
        #	Achternaam = Naam.split(" ", 1)[0]
        #	Naam = Naam.replace(Achternaam, '') + " " + Achternaam
        Adres = td[1].text.strip()
        Woonplaats = td[2].text.strip()
        UBN = td[3].text.strip()
        VNLid = td[4].text.strip()
        Telefoonnr = td[5].text.strip()
        Email = td[6].text.strip()

        fokker[id] = {}
        fokker[id]["id"] = id
        fokker[id]["adres"] = Adres
        if len(Woonplaats) > 0: fokker[id]["woonplaats"] = Woonplaats
        if len(UBN) > 0: fokker[id]["UBN"] = UBN
        if len(VNLid) > 0: fokker[id]["VNLid"] = VNLid
        if len(Telefoonnr) > 0: fokker[id]["telefoonnr"] = Telefoonnr
        if len(Email) > 0: fokker[id]["email"] = Email

    except (ValueError, AttributeError, IndexError):
        errors += 1
        pass

state["leeft"] = []
state["fokker_op_id"] = fokker
state["first_2"] = True         # Signal the stage2 crawler that its its first run.

with open("state.json", 'w', encoding='utf-8') as f:
	json.dump(state, f, sort_keys=True, ensure_ascii=False, indent=2)

print(f"Parsed {len(fokker)} breeders, skipped {errors} errors.")
