# stamboek_wiltshire

A analysis toolkit and crawler for maintaining a sheep pedigree dataset.

The project collects data from a web-based pedigree system, keeps it up to date over time, and provides tools to explore and validate the data.

---

## Overview

This project was built to support a practical goal:

> selecting the most suitable ram lamb for breeding, based on pedigree data.

To achieve this, the system:

* collects data from a web-based pedigree system
* maintains a local dataset of sheep and their relationships
* computes metrics such as inbreeding, fertility, relatedness
* allows comparing all breeding animals in a consistent way

The crawler incrementally builds and updates the dataset, while analysis scripts use that data to evaluate and rank animals for breeding decisions.

Rather than a one-time scraper, this is a **stateful system** designed to:

* run periodically
* keep data up to date
* support real-world decision making using imperfect data

---

## Example Output

The analysis scripts are used to support breeding decisions.

For example, ranking ram lambs based on expected inbreeding when crossed with specific ewes:

```
Inbreeding for ram lambs (< 1 year),
crossed with all ewes of owner OWNER.

ID         ewe 1      ewe 2      average  owner
---------------------------------------------------
RAM-001    0.94 %     1.18 %     1.06 %   Breeder A
RAM-002    1.23 %     1.35 %     1.29 %   Breeder B
RAM-003    1.15 %     1.47 %     1.31 %   Breeder A
RAM-004    1.87 %     2.59 %     2.23 %   Breeder C
RAM-005    2.64 %     2.30 %     2.47 %   Breeder D
...
RAM-020    4.79 %     7.60 %     6.20 %   Breeder E
RAM-021    5.15 %     7.80 %     6.47 %   Breeder C
```

---

## Structure

### `/crawler`

Core crawling pipeline:

* `md_parse_breeder_list.py`
* `md_crawl_breeder_sheeplist.py`
* `md_crawl_sheep.py`

These scripts discover breeders, collect current stock, and expand sheep records.

See `/crawler/README.md` for details.

---

### `/tools`

Maintenance and validation:

* detecting missing identifiers
* cleaning inconsistent relationships
* repairing incomplete records

These scripts keep the dataset usable over time.

---

### Analysis scripts

The root directory contains scripts that work directly on the dataset:

* `statistiek.py` — general statistics per breed
* `genotypes.py` — Scrapie resistence genotype distribution
* `inteelt.py`, `inteelt_statistiek.py` — inbreeding analysis, crossing a single breeders ewes to all of the breeds lambs
* `verwantschap.py` — calculates relatedness for all rams in a breed 
* `leeftijd_wsh*.py` — Suspiciously old Wiltshire Horns
* `worpindex_maand.py`, `worpindex_ras.py` — lambing metrics, per month or per ageyear

Additional utilities:

* `zoek_schaap.py`, `zoek_fokker.py` — lookup tools
* `status.py`, `punten.py`, `naam.py` — small data queries

These scripts are not required for crawling, but show how the dataset can be used.

---

## Data Files

### `db.json`

The main dataset:

* `schaap` → sheep records
* `fokker` → breeder records


---

### `state.json`

Crawler state:

* `todo` → sheep to process
* `done` → processed sheep
* `alive` → currently observed sheep

---

## How It Works

1. Parse breeder list
2. Crawl breeder sheep lists
3. Crawl individual sheep and expand relations

The crawler can be run periodically to keep the dataset current.

---

## Requirements

* Python 3
* `beautifulsoup4`
* `html5lib`

---

## Notes

* Requires a login (`login.py`, not included)
* Use `login_example.py` as a template
* The dataset is not included. It can be reconstructed with the crawler and valid credentials for the pedigree website.
* Data reflects real-world entry and may change over time
* Inbreeding calculation is based on an simplified calculation, it is not the exact scientific inbreeding coefficient.

---

## Summary

This project focuses on maintaining a usable dataset from imperfect external data, combining:

* incremental crawling
* data validation
* analysis tools

