#!/bin/python3

# Berekent inteelt voor al de schapen in de database

import inteelt, json 

#def ptree(db, s):
# Builds parent tree for sheep id s
# Returns: dict of parents and genetic contribution
# parent: 0.5, parent's parent: 0.25, parent's parent's parent 0.125 etc...
# Note that conribution sum is more than 1, the sum of each 
# known generation is 1.

#def bereken_inteelt_coefficient(o, r):

def main():
	print("Berekent inteelt voor alle schapen in de database.")
	
	# Open schapen db
	with open("../db.json") as f:
		db = json.load(f)

	# Per schaap, bereken de inteelt
	for id in db["schaap"]:
		try:
			s = db["schaap"][id]
			if "inteelt" in s:
				continue
			vader = s["vader_id"]
			moeder = s["moeder_id"]
			#print(id)
			s["inteelt"] = inteelt.bereken_inteelt_coefficient(db, moeder, vader)
			print(".", end="", flush=True)
		except KeyError:
			#print("error is terror")
			s["inteelt"] = 0

	# DB opslaan
	print("XXXXXXXXXXXXXXXXX   Storing DB  XXXXXXXXXXXXXXXXX")
	with open("../db.json", 'w', encoding='utf-8') as f:
		json.dump(db, f, sort_keys=True, ensure_ascii=False, indent=2)
	print("XXXXXXXXXXXXXXXXXXXX   Done  XXXXXXXXXXXXXXXXXXXX")

	return

if __name__ == "__main__":
	main()










	
































