# 🧬 DNA Sequences QC – Beginner 🐍

Introductory exercise on **data quality in bioinformatics**: load DNA sequences, check for common issues (duplicate IDs, null values, invalid characters), and perform basic cleaning.

## 🎯 Learning Objectives
- 📥 Load data using **pandas**.
- 🔍 Check data quality with `duplicated()`, `isna()`, `str.match()` and regular expressions.
- ⚙️ Use `if` statements to report and act on findings.
- 🧽 Clean sequences (trim, uppercase, `U→T`, remove non-ACGT) and produce a clean dataset.

## 📂 Dataset
File with intentional errors: `data/dna_sequences_bad.csv`  
It includes duplicate IDs, empty sequences or sequences with leading/trailing spaces, lowercase letters, characters outside **A/C/G/T** (e.g., `N`, dashes), and RNA letters (`U`).  
**Note:** Errors are embedded directly in the sequences (no inline comments in the CSV).

It contains:
- 🆔 Duplicate IDs
- ⬜ Empty sequences or sequences with leading/trailing spaces
- 🔠 Lowercase letters
- ❌ Characters outside A/C/G/T (e.g., N, dashes)
- 🧬 RNA letters (U)

## 📋 Requirements
See `requirements.txt`

## 🖥️ How to Run

### default CSV (data/dna_sequences_bad.csv)
python sequence_quality_checker.py

### custom CSV
python sequence_quality_checker.py --csv path/to/your.csv

### strict mode (exit 1 if any QC error is found)
python sequence_quality_checker.py --strict

### show cleaning preview in the console
python sequence_quality_checker.py --show-clean


## 📊 What the script does

1. Prints dataset size and first rows.

2. Computes basic length statistics (without adding columns to the DataFrame).

3. Runs quality checks:

    Duplicate IDs
    Null/empty sequences
    Formatting issues (leading/trailing spaces, lowercase, presence of U)
    Invalid characters (anything outside A/C/G/T)

4. Cleans sequences (trim, uppercase, U→T, strip non-ACGT).

5. Filters out sequences still invalid after cleaning.

6. Saves a clean two-column CSV as dna_sequences_clean.csv next to the input file:

...
id,sequence
seq1,ATGCGTACGTTAG
seq2,GGGTTTCCCAAAGG
...


