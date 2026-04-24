#!/bin/python3
import json, datetime
fokker =    "BREEDER_NAME_HERE"

def main():
    
    with open("db.json") as f:
        db = json.load(f)
 
    print(f"Stallijst {fokker}")
    print("Fokkerij nummer: {}".format(db["fokker"][fokker]["VNLid"]))
    print("UBN: {}".format(db["fokker"][fokker]["UBN"]))
    print("Adres: {} {}".format(db["fokker"][fokker]["adres"], db["fokker"][fokker]["woonplaats"]))
    print("Datum: {}".format(datetime.datetime.now().strftime("%d/%m/%Y")))
    print("")
    print("                     geslacht status                            lammeren")
    print("nr stamboeknr  levensnr     | | geboren    vader       moeder   worpen |")
    for i, s_id in enumerate(db["fokker"][fokker]["stal"], start=1):
        s = db["schaap"][s_id]
        worpen = s.get("Aantal worpen", "")
        lammeren = s.get("Aantal lammeren", "")
        print(  f"{i:2} {s['VNLid']:11} {s['LevensNr']:12} {s['Geslacht']:1} {s['Status']:1} "
                f"{s['Gebdat']:10} {s['Vader']:11} {s['Moeder']:11} {worpen:2} {lammeren:2}")

if __name__ == "__main__":
	main()










	
































