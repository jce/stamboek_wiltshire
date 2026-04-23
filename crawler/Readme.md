# Crawler

This folder contains the core crawling logic used to build and maintain the pedigree database.

The crawler operates in **three stages**, each with a specific responsibility. Together they form a pipeline that incrementally discovers, expands, and updates sheep records.

---

## Overview

The system is designed to:

* Collect data from a web-based pedigree system
* Maintain a local dataset (`db.json`)
* Handle incomplete and evolving records
* Support repeated crawls without losing data integrity

The crawler separates:

* **Database (`db.json`)** → the actual data
* **State (`state.json`)** → what still needs to be processed

---

## Stages

### Stage 1 — Breeder List Parsing

* Manually download the breeder list.

**Script:** `md_parse_breeder_list.py`

* Parses a locally saved breeder list (HTML)
* Extracts breeder identifiers and metadata
* Initializes crawler state

Output:

* Stores breeder data in `state.json`

---

### Stage 2 — Breeder Sheep Lists

**Script:** `md_crawl_breeder_sheeplist.py`

* Logs into the pedigree website
* Fetches the current stock list for each breeder
* Identifies sheep that are currently alive

Output:

* Updates `state.json`:

  * `alive` → sheep currently present in breeder stock lists
  * `todo` → sheep to be processed in Stage 3

* Updates `db.json`:
  
  * `breeder` - Breeder information
  * `sheep` - Placeholders for existing sheep
---

### Stage 3 — Sheep Expansion

**Script:** `md_crawl_sheep.py`

* Crawls individual sheep pages

* Extracts detailed information:

  * identifiers (levensnummer, VNLid, etc.)
  * parent relations
  * name
  * scores

* Expands the dataset by following relations (parents, children)

Output:

* Updates `db.json` with full sheep records
* Updates `state.json`:

  * removes processed sheep from `todo`
  * adds them to `done`

---

## Data Model

### `db.json`

Contains the persistent dataset:

* `schaap` → all sheep records
* `fokker` → breeder data

This file is considered the **source of truth**.

---

### `state.json`

Tracks crawler progress:

* `todo` → sheep IDs to process
* `done` → already processed sheep
* `alive` → sheep observed as alive in latest crawl

This file can be modified or reset without losing core data.

---

## Design Notes

* The crawler is **incremental**: it can be run multiple times to update data
* Data is intentionally **overwritten** when re-fetching a sheep to reflect changes
* Incomplete or inconsistent data can occur due to:

  * upstream data entry
  * timing of crawls
  * transient failures

Separate tools exist to detect and repair such cases.

---

## Requirements

* Python 3
* `beautifulsoup4`
* `html5lib`

---

## Usage (typical workflow)

1. Download the breeders' page. Run `md_parse_breeder_list.py` to load breeders
2. Run `md_crawl_breeder_sheeplist.py` to discover active sheep. Takes 1 ~ 2 hours.
3. Run `md_crawl_sheep.py` to expand and update the dataset. Takes some more hours.

The crawler is typically run periodically to keep the dataset up to date.

---

## Notes

* The crawler depends on a valid login (`login.py`, not included in repo)
* Use `login_example.py` as a template
* Website IDs are used as primary keys for crawling

---

## Summary

This crawler is not a one-time scraper, but a **stateful system** designed to:

* maintain a growing dataset
* handle real-world inconsistencies
* support long-term incremental updates

