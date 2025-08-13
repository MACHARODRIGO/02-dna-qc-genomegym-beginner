# 🧬 DNA Sequences QC – Beginner 🐍

Introductory exercise on **data quality in bioinformatics**: load DNA sequences, check for common issues (duplicate IDs, null values, invalid characters), and perform basic cleaning.

## 🎯 Learning Objectives
- 📥 Load data using **pandas**.
- 🔍 Check data quality with `duplicated()`, `isna()`, `str.match()`, and regular expressions.
- ⚙️ Implement conditional logic with `if` to report and act on findings.
- 🧽 Generate a “clean” sequence column.

## 📂 Dataset
File with intentional errors: `data/dna_sequences_bad.csv`

It contains:
- 🆔 Duplicate IDs
- ⬜ Empty sequences or sequences with leading/trailing spaces
- 🔠 Lowercase letters
- ❌ Characters outside A/C/G/T (e.g., N, dashes)
- 🧬 RNA letters (U)

## 📋 Requirements
See `requirements.txt`

## 🖥️ How to Run

From the repository root:

```bash
python explore_dataset.py --csv data/dna_sequences_bad.csv

