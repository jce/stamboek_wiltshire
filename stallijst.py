#!/bin/python3
import json
fokker =    "BREEDER_NAME_HERE"

def main():
    
    with open("db.json") as f:
        db = json.load(f)
 
    print(f"Stallijst {fokker}")
    print("Fokkerij nummer: {}".format(db["fokker"][fokker]["VNLid"]))
    print("UBN: {}".format(db["fokker"][fokker]["UBN"]))
    print("Adres: {} {}".format(db["fokker"][fokker]["adres"], db["fokker"][fokker]["woonplaats"]))
    print("")
    print("                     geslacht status                              lammen")
    print("nr stamboeknr  levensnr     | | geboren    vader       moeder   worpen |")
    i = 0
    for s in db["fokker"][fokker]["stal"]:
        i += 1
        VNLid = db["schaap"][s]["VNLid"]
        LevensNr = db["schaap"][s]["LevensNr"]
        Geslacht = db["schaap"][s]["Geslacht"]
        Status = db["schaap"][s]["Status"]
        Gebdat = db["schaap"][s]["Gebdat"]
        Vader = db["schaap"][s]["Vader"]
        Moeder = db["schaap"][s]["Moeder"]
        print("{:2} {:11} {:12} {:1} {:1} {:10} {:11} {:11}".format(i, VNLid, LevensNr, Geslacht, Status, Gebdat, Vader, Moeder), end="")
        try:
            print(" {:2}".format(db["schaap"][s]["Aantal worpen"]), end="")
        except KeyError:
            print("   ", end="")
        try:
            print(" {:2}".format(db["schaap"][s]["Aantal lammeren"]), end="")
        except KeyError:
            print("    ", end="")
        print("")

if __name__ == "__main__":
	main()










	
































