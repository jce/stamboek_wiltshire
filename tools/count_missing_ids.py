#!/bin/python3
import datetime, json, sys

with open("../db.json") as f:
	db = json.load(f)

count_all = 0
count_2ids = 0
count_lifenr_missing = 0
count_VNLid_missing = 0
count_both_missing = 0
lifenr = {}
VNLid = {}
lifedouble = []
VNLdouble = []
count_ln_double = 0
count_VNLid_double = 0

for i in db["schaap"]:
    schaap = db["schaap"][i]
    count_all = count_all + 1
    have_lifenr = "LevensNr" in schaap and schaap["LevensNr"] != ""
    have_VNLid = "VNLid" in schaap and schaap["VNLid"] != ""

    if have_lifenr and have_VNLid:
        count_2ids = count_2ids + 1
    if have_lifenr and not have_VNLid:
        count_VNLid_missing = count_VNLid_missing + 1
    if not have_lifenr and have_VNLid:
        count_lifenr_missing = count_lifenr_missing + 1
    if not have_lifenr and not have_VNLid:
        count_both_missing = count_both_missing + 1
    
    if have_lifenr:
        if schaap["LevensNr"] in lifenr:
            count_ln_double = count_ln_double + 1
            lifedouble.append(schaap["LevensNr"])
        lifenr[schaap["LevensNr"]] = True
    if have_VNLid:
        if schaap["VNLid"] in VNLid:
            count_VNLid_double = count_VNLid_double + 1
            VNLdouble.append(schaap["VNLid"])
        VNLid[schaap["VNLid"]] = True

print("Sheep: {}".format(count_all))
print("2 ids: {}".format(count_2ids))
print("Lifenr missing: {}".format(count_lifenr_missing))
print("VNLid missing: {}".format(count_VNLid_missing))
print("Both missing: {}".format(count_both_missing))
print("Lifenr double: {}".format(count_ln_double))
print("VNLid double: {}".format(count_VNLid_double))
print("Lifenr double: {}".format(lifedouble))
print("VNLid double: {}".format(VNLdouble))










	
































