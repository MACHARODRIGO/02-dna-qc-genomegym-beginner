import pandas as pd
import re
import argparse
import sys
import os

# ------------------------
# Argument parsing
# ------------------------
parser = argparse.ArgumentParser(
    description="DNA Sequences QC – Beginner: Load sequences, run quality checks, clean, and save results."
)
parser.add_argument(
    "--csv",
    default="data/dna_sequences_bad.csv",
    help="Path to input CSV file (default: data/dna_sequences_bad.csv)"
)
parser.add_argument(
    "--show-clean",
    action="store_true",
    help="Show preview of cleaned sequences"
)
parser.add_argument(
    "--strict",
    action="store_true",
    help="Exit with code 1 if any QC error is found"
)
args = parser.parse_args()

csv_path = args.csv

# ------------------------
# 📥 Load dataset
# ------------------------

if not os.path.exists(csv_path):
    print(f"⛔ Input file not found: {csv_path}")
    sys.exit(1)
if os.path.getsize(csv_path) == 0:
    print(f"⛔ Input CSV is empty: {csv_path}")
    sys.exit(1)


df = pd.read_csv(csv_path)

print(f"\n📊 Total sequences: {len(df)}\n")
print("👀 First sequences:")
print(df.head())

# ------------------------
# 📏 Length statistics
# ------------------------
lengths = df["sequence"].fillna("").str.len()

print("\n📈 Length statistics:")
print(lengths.describe())

mean_len = lengths.mean()
long_mask = lengths > mean_len

print("\n⬆️ Sequences longer than the mean:")
# join the computed lengths only for display
print(
    pd.concat(
        [df.loc[long_mask, ["id", "sequence"]], lengths[long_mask].rename("length")],
        axis=1
    )
)

# -----------------------------
# 🛡️ Quality Checks
# -----------------------------

print("\n=== 🧪 Quality checks ===")

# 1) 🆔 Duplicate IDs
dup_mask = df["id"].duplicated(keep=False)
dup_count = dup_mask.sum()
print(f"🔍 Duplicate IDs: {dup_count}")
if dup_count:
    print(df.loc[dup_mask, ["id", "sequence"]].sort_values("id"))

# 2) ⬜ Null or empty values in 'sequence'
null_or_empty = df["sequence"].isna() | (df["sequence"].astype(str).str.strip() == "")
null_count = null_or_empty.sum()
print(f"\n🔍 Null or empty 'sequence': {null_count}")
if null_count:
    print(df.loc[null_or_empty, ["id", "sequence"]])

# 3) ❌ Invalid characters (only A/C/G/T allowed)
#    Also detect common formatting issues
leading_trailing_ws = df["sequence"].astype(str).str.match(r"^\s|\s$")
lowercase_mask = df["sequence"].astype(str).str.contains(r"[acgt]", regex=True)
has_U = df["sequence"].astype(str).str.contains("U", regex=False)

invalid_regex = r"^[ACGT]+$"
invalid_mask = ~df["sequence"].astype(str).str.upper().str.match(invalid_regex)

print(f"\n🔍 Sequences with leading/trailing spaces: {leading_trailing_ws.sum()}")
print(f"🔍 Sequences with lowercase letters: {lowercase_mask.sum()}")
print(f"🔍 Sequences containing 'U' (RNA): {has_U.sum()}")
print(f"🔍 Sequences with invalid characters (outside A/C/G/T): {invalid_mask.sum()}")

if invalid_mask.any():
    print(df.loc[invalid_mask, ["id", "sequence"]])

# ------------------------
# 🧽 Quick cleaning function
# ------------------------

def clean_seq(s: str) -> str:
    if pd.isna(s):
        return s
    s = s.strip()                  # remove spaces
    s = s.upper()                  # to uppercase
    s = s.replace("U", "T")        # RNA -> DNA
    s = re.sub(r"[^ACGT]", "", s)  # keep only A/C/G/T
    return s

seq_clean = df["sequence"].apply(clean_seq)
still_invalid = ~seq_clean.astype(str).str.match(invalid_regex)

if args.show_clean:
    print("\n🧽 'sequence_clean' preview (post-cleaning):")
    df_preview = df.loc[:, ["id", "sequence"]].copy()
    df_preview["sequence_clean"] = seq_clean
    print(df_preview)

print(f"\n🔁 Still invalid after cleaning: {int(still_invalid.sum())}")
if still_invalid.any():
    bad_preview = df.loc[still_invalid, ["id", "sequence"]].copy()
    bad_preview["sequence_clean"] = seq_clean[still_invalid]
    print(bad_preview)

# ------------------------
# 🔄 Interactive duplicate-ID resolution
# ------------------------
if dup_count:
    print("\n⚠️  Duplicate IDs detected. Let's fix them interactively.")
    print("   Tip: IDs like 'seq8' or 'seq9' are fine, but any unique string is accepted.\n")

    used_ids = set(df["id"].astype(str))

    for id_value, idxs in df.groupby("id", sort=False).indices.items():
        if len(idxs) <= 1:
            continue
        first_idx = idxs[0]
        first_line = first_idx + 2

        for idx in idxs[1:]:
            src_line = idx + 2
            while True:
                new_id = input(
                    f"🟡 Duplicate ID '{id_value}' found at line {src_line} "
                    f"(first occurs at line {first_line}). Please enter a NEW unique ID: "
                ).strip()
                if not new_id:
                    print("   ⛔ Empty ID is not allowed. Try again.")
                    continue
                if new_id in used_ids:
                    print(f"   ⛔ '{new_id}' already exists. Please choose a different ID.")
                    continue
                df.at[idx, "id"] = new_id
                used_ids.add(new_id)
                print(f"   ✅ Updated line {src_line}: id -> '{new_id}'")
                break

    dup_mask_after = df["id"].duplicated(keep=False)
    if dup_mask_after.any():
        print("\n⛔ There are still duplicate IDs after manual edits. Please re-run and fix remaining ones.")
        sys.exit(1)
    print("\n✅ All duplicate IDs resolved.")

# ------------------------
# 💾 Save clean dataset
# ------------------------

df_out = df.loc[~still_invalid, ["id"]].copy()
df_out["sequence"] = seq_clean[~still_invalid].values

out_path = os.path.join(os.path.dirname(csv_path) or ".", "dna_sequences_clean.csv")
df_out.to_csv(out_path, index=False)

print("\n✅ Clean dataset (2 columns):")
print(df_out)
print(f"\n💾 Clean dataset saved to '{out_path}'")

# ------------------------
# Strict mode exit
# ------------------------
qc_error_found = any([
    dup_count > 0,
    null_count > 0,
    invalid_mask.sum() > 0
])
if qc_error_found and args.strict:
    print("\n⛔ QC errors detected. Exiting due to --strict.")
    sys.exit(1)