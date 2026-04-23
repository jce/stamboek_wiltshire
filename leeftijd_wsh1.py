#!/bin/python3

# Zoek de leeftijdsverdeling bij wiltshire horns
agemax = 20

import json, datetime

nu = datetime.datetime.now().date()
with open("db.json") as f:
    db = json.load(f)

ras = "Wiltshire Horn"

def main():
    leeftijd = [0] * (agemax+1)
    for sid in db["schaap"]:
        s = db["schaap"][sid]
        try:
            geboren = datetime.datetime.strptime(s["Gebdat"], '%d/%m/%Y').date()
            s["leeftijd"] = nu - geboren
            if s["Ras"] == ras and s["leeft"] :
                l = int(s["leeftijd"].days / 365)
                leeftijd[l] = leeftijd[l] + 1
        except KeyError:
            pass

    print("Leeftijd Aantal {}".format(ras))
    for l in range(agemax+1):
        print("{:2}       {:4}".format(l, leeftijd[l]))

if __name__ == "__main__":
    main()



















