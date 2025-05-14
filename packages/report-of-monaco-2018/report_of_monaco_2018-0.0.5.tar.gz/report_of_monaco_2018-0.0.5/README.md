# 🏎️ Monaco F1 2018 Q1 Lap Report

A command-line tool to analyze the best lap times of Formula 1 drivers during **Q1 (first qualification stage)** of the **Monaco Grand Prix 2018**.

This tool parses log files with start and end timestamps of the best laps (first 20 minutes only), calculates lap durations, and generates a clean, formatted report of the top 15 drivers who advance to Q2 — and those who don't.

---

## 📁 Dataset

The application works with the following three files:

- `abbreviations.txt`: contains driver abbreviations, full names, and team names.
- `start.log`: contains timestamps of when each driver's start race.
- `end.log`: contains timestamps of when each driver's end race.

### Example entry for start.log and end.log files:
SVF2018-05-24_12:02:58.917


- `SVF`: Driver abbreviation  
- `2018-05-24`: Date  
- `12:02:58.917`: Start or end time (used for lap duration calculation)

---
### Example entry for abbreviations.txt:
DRR_Daniel Riccardo_RED BULL RACING TAG HEUER

- `DRR`:  Driver abbreviation 
- `Daniel Riccardo`: Driver name
- `RED BULL RACING TAG HEUER`: Driver team

## 🏁 Report Example

After parsing and calculating lap times, the output will look like:

```
1. Daniel Ricciardo      | RED BULL RACING TAG HEUER     | 1:12.013

2. Sebastian Vettel      | FERRARI                                            | 1:12.415

3. ...

------------------------------------------------------------------------

16. Brendon Hartley   | SCUDERIA TORO ROSSO HONDA | 1:13.179

17. Marcus Ericsson  | SAUBER FERRARI                            | 1:13.265

```
## Instalation 
Report-of-monaco-2018 can be installed by running `pip install report-monaco==0.0.5`. 
It requires Python 3.9+ to run.

## 🔧 Features

- Calculates and sorts drivers by best lap time.
- Separates top 15 drivers from the rest.
- Command-line interface to choose sorting order or filter by driver.
- Graceful error handling (missing files, invalid data).


---

## 💻 Usage

Install dependencies and run the CLI app:

## Examples:

```bash
 `report-monaco --file data --desc`
 `report-monaco --file data --driver "Sebastian Vettel"`
```
# Options:
--file <path>(./data): Path to the folder containing the start.log, end.log, and abbreviations.txt files.

--asc: Sort report in ascending order (default).

--desc: Sort in descending order.

--driver "<name>": Show info for a specific driver.

### License
MIT


