#!/bin/python3
import json

def test_for_parent(sheep_id, sheep, partype, partype2):
    if sheep.get(partype) == sheep_id:
        print(f"Sheep {sheep_id} references itself as {partype}. Fixing...")
        print(json.dumps(sheep, indent=2, ensure_ascii=False))
        sheep.pop(partype, None)
        sheep.pop(partype2, None)

def main():

    print("Cleans database of sheep referencing themselves as father or mother.")
	
    with open("db.json") as f:
        db = json.load(f)

    for sheep_id, sheep in db["schaap"].items():
        test_for_parent(sheep_id, sheep, "vader_id", "Vader")
        test_for_parent(sheep_id, sheep, "moeder_id", "Moeder")

    print("XXXXXXXXXXXXXXXXX   Storing DB  XXXXXXXXXXXXXXXXX")
    with open("db.json", 'w', encoding='utf-8') as f:
        json.dump(db, f, sort_keys=True, ensure_ascii=False, indent=2)
    print("XXXXXXXXXXXXXXXXXXXX   Done  XXXXXXXXXXXXXXXXXXXX")

if __name__ == "__main__":
    main()










	
































