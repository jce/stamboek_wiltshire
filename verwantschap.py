#!/bin/python3

# Calculates relatedness for all living Wiltshire Horn rams
# to the population of living Wiltshire Horns, that is the percentage
# of the total gene pool that is equal to those of the individual.

# Sets a zero relationship-coefficient (rc) to all sheep.
def set_all_rc_zero(db):
    for i in db["schaap"]:
        db["schaap"][i]["rc"] = 0   # relation coefficient

# Adds the rc for an individual, recurse to parents.
def add_rc_parent(sheep_id, rc, parents, db):
    parents.add(sheep_id)
    s = db["schaap"][sheep_id]
    s["rc"] = s["rc"] + rc
    if "vader_id" in s:
        add_rc_parent(s["vader_id"], rc/2, parents, db)
    if "moeder_id" in s:
        add_rc_parent(s["moeder_id"], rc/2, parents, db)

# Sets the rc to an individual's children, recurse to children. Ignores
# parents.
def set_rc_child(sheep_id, parents, db):
    s = db["schaap"][sheep_id]

    if sheep_id not in parents:
        rcf = 0
        if "vader_id" in s:
            rcf = db["schaap"][s["vader_id"]]["rc"]
        rcm = 0
        if "moeder_id" in s:
            rcm = db["schaap"][s["moeder_id"]]["rc"]
        s["rc"] = rcf/2 + rcm/2

    if "kind" in s:
        for cid in s["kind"]:
            if cid not in parents:
                # This gets called more often than necessary, for example if
                # both parents are related.
                set_rc_child(cid, parents, db)

# Calculate the relatedness of one individual with the living population.
def relatedness(iut, db): # iut = individual under test.

    set_all_rc_zero(db)
    parents = set()
    # Step 1: upwards calculation. For every parent, the genetic contribution is
    # half that of the current individual. Parents can form loops, contribution
    # is additive in this case.
    add_rc_parent(iut, 1, parents, db)
    # Step 2: downwards calculation. Starting at every parent, calculate the
    # contribution to all children, and childrens children. This is
    # deterministic.
    for parent in parents:
        set_rc_child(parent, parents, db)

    # Calculate the genetic presence within the living population.
    race = db["schaap"][iut]["Ras"]
    count = 0
    sum = 0
    for sheep_id in db["schaap"]:
        s = db["schaap"][sheep_id]
        if "Ras" in s and s["Ras"] == race and s["leeft"]:
            count = count + 1
            sum = sum + s["rc"]

    return sum/count

def main():
    import json

    ras = "Wiltshire Horn"
    #ras = "Coburger Fuchs"
    #ras = "Charmoise"
    #ras = "Walliser Schwarznase"

    with open("db.json") as f:
        db = json.load(f)

    # Voor alle wiltshire horn rammen, wat is hun relatedness
    sheeprelated = {}
    for schaap_id in db["schaap"]:
        s = db["schaap"][schaap_id]
        try:
            if s["Ras"] == ras and s["Geslacht"] == "M" and s["leeft"]:# and s["Status"] == "V":
                if db["schaap"][s["vader_id"]]["Status"] == "V":                                                              
                    if db["schaap"][s["moeder_id"]]["Status"] == "V":
                        sheeprelated[schaap_id] = relatedness(schaap_id, db)
                        print(".", end="", flush=True)
        except KeyError:
            pass
 
    sheeprelated = dict(sorted(sheeprelated.items(), key=lambda item: item[1]))

    print("\nSchaap   Verwantschap [%]")
    for s in sheeprelated:
        print("{}   {:.3f}".format(db["schaap"][s]["VNLid"], sheeprelated[s]*100))

if __name__ == "__main__":
    main()
	
































