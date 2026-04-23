#!/bin/python3

print("Test voor alle ouders of ze dit individu als kind hebben.")

import json, datetime
with open("../db.json") as f:
	db = json.load(f)

def find_id(VNLid):
	for s in db["schaap"]:
		if db["schaap"][s]["VNLid"] == VNLid:
			return s
	return None

for s in db["schaap"]:
	schaap = db["schaap"][s]
	if "Moeder" in schaap:
		moeder = schaap["Moeder"]
		mid = find_id(moeder)
		if not mid:
			print("{}: moeder ({}) niet gevonden.".format(s, moeder))
		else:
			if not "kind" in db["schaap"][mid]:
				print("{}: moeder ({}) heeft geen kinderen.".format(s, moeder))
			else:
				if not s in db["schaap"][mid]["kind"]:
					print("{} is kind van {} maar staat niet bij kinderen.".format(s, moeder))
	if "Vader" in schaap:
		vader = schaap["Vader"]
		vid = find_id(vader)
		if not vid:
			print("{}: vader ({}) niet gevonden.".format(s, vader))
		else:
			if not "kind" in db["schaap"][vid]:
				print("{}: vader ({}) heeft geen kinderen.".format(s, vader))
			else:
				if not s in db["schaap"][vid]["kind"]:
					print("{} is kind van {} maar staat niet bij kinderen.".format(s, vader))

print("Done")










	
































