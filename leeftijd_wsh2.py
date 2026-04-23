#!/bin/python3

# Zoek de leeftijdsverdeling bij wiltshire horns
agemin = 7
agemax = 20
wrap = 5
 
import json, datetime

nu = datetime.datetime.now().date()
with open("db.json") as f:
    db = json.load(f)

ras = "Wiltshire Horn"

def main():
    leeftijd = [ [] for _ in range(agemax+1) ]
    for sid in db["schaap"]:
        s = db["schaap"][sid]
        try:
            if s["Ras"] == ras and s["leeft"] :
                geboren = datetime.datetime.strptime(s["Gebdat"], '%d/%m/%Y').date()
                l = int( (nu - geboren).days / 365)
                leeftijd[l].append(s)
        except KeyError:
            pass
    
    for i in range(agemax + 1):
        leeftijd[i] = sorted(leeftijd[i], key=lambda d: d["VNLid"])

    print("Leeftijd, Aantal {}, individuen ({} - {} jaar)".format(ras, agemin, agemax))
    for l in range(agemax+1):
        print("{:2}       {:4}".format(l, len(leeftijd[l])), end="")
        if l >= agemin:
            w = 0
            for i in leeftijd[l]:
                if w >= wrap:
                    print("\n             ", end="")
                    w = 0
                print(" {}".format(i["VNLid"]), end="")
                w = w + 1
        print("")

if __name__ == "__main__":
    main()


