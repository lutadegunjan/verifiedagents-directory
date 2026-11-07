import pandas as pd
import sqlite3
import json
import os
import time
from pathlib import Path

BASE = Path("extraction_workspace")
BATCH = BASE / "pending_batch_50000.csv"
MASTER = BASE / "verifiedagents_consolidated.csv"
INPUT = BASE / "manual_exports"
OUTPUT = BASE / "verifiedagents_50k_processed.csv"
CHECKPOINT = BASE / "verifiedagents_50k_checkpoint.json"

BATCH_SIZE = 50000
MAX_WORKERS = 10  # Configuration; pandas vectorization handles this workload.

COLUMNS = [
    "profile_page_url", "full_name", "npn_number", "location",
    "phone_numbers", "email_addresses", "websites",
    "appointed_companies", "scraped_by"
]

def norm_url(series):
    return series.fillna("").astype(str).str.strip().str.rstrip("/")

def atomic_csv(df, path):
    temp = path.with_suffix(".tmp.csv")
    df.to_csv(temp, index=False)
    os.replace(temp, path)

def main():
    start = time.perf_counter()

    for path in (BATCH, MASTER):
        if not path.exists():
            raise FileNotFoundError(path)

    if not INPUT.exists():
        INPUT.mkdir(parents=True)

    batch = pd.read_csv(BATCH, dtype=str).fillna("")
    master = pd.read_csv(MASTER, dtype=str).fillna("")

    if len(batch) > BATCH_SIZE:
        raise ValueError("Pending batch exceeds 50,000 rows.")

    if batch.npn_number.duplicated().any():
        raise ValueError("Duplicate NPNs in pending batch.")

    con = sqlite3.connect(BASE / "extraction_tracker.db")
    try:
        tracker = pd.read_sql_query("""
            SELECT profile_url, npn
            FROM profiles
            WHERE status = 'extracted'
        """, con)
    finally:
        con.close()

    tracker["npn"] = tracker["npn"].astype(str).str.strip()
    tracker["url_norm"] = norm_url(tracker["profile_url"])

    tracker_pairs = set(zip(tracker["npn"], tracker["url_norm"]))

    existing_npns = set(master.npn_number.astype(str).str.strip())
    existing_urls = set(norm_url(master.profile_page_url))

    frames = []
    for file in sorted(INPUT.glob("*.csv")):
        df = pd.read_csv(file, dtype=str).fillna("")
        missing = set(COLUMNS) - set(df.columns)

        if missing:
            print("SKIPPED:", file.name, "| Missing:", sorted(missing))
            continue

        df = df[COLUMNS].copy()
        for col in COLUMNS:
            df[col] = df[col].fillna("").astype(str).str.strip()

        print("READ:", file.name, "| ROWS:", len(df))
        frames.append(df)

    if not frames:
        print("No compatible CSV exports found.")
        return

    incoming = pd.concat(frames, ignore_index=True)
    incoming["npn_number"] = incoming.npn_number.astype(str).str.strip()
    incoming["_url_norm"] = norm_url(incoming.profile_page_url)

    valid_mask = [
        (npn, url) in tracker_pairs
        for npn, url in zip(incoming.npn_number, incoming._url_norm)
    ]

    valid = incoming.loc[valid_mask].copy()
    invalid_count = len(incoming) - len(valid)

    valid = valid.drop_duplicates("npn_number", keep="last")
    valid = valid[
        ~valid.npn_number.isin(existing_npns)
        & ~valid._url_norm.isin(existing_urls)
    ]

    valid = valid[valid.npn_number.ne("") & valid._url_norm.ne("")]
    valid["scraped_by"] = "Gunjan Lutade"

    new_records = valid[COLUMNS].copy()

    processed_path = OUTPUT
    if processed_path.exists():
        previous = pd.read_csv(processed_path, dtype=str).fillna("")
        for col in COLUMNS:
            previous[col] = previous[col].astype(str).str.strip()
        combined = pd.concat([previous[COLUMNS], new_records], ignore_index=True)
    else:
        combined = pd.concat([master[COLUMNS], new_records], ignore_index=True)

    combined["_url_norm"] = norm_url(combined.profile_page_url)
    combined = combined.drop_duplicates("npn_number", keep="first")
    combined = combined.drop_duplicates("_url_norm", keep="first")
    combined = combined.drop(columns="_url_norm")

    if combined.npn_number.duplicated().any():
        raise RuntimeError("Duplicate NPN audit failed.")

    if norm_url(combined.profile_page_url).duplicated().any():
        raise RuntimeError("Duplicate URL audit failed.")

    atomic_csv(combined, OUTPUT)

    checkpoint = {
        "batch_size": len(batch),
        "tracker_extracted": len(tracker),
        "input_records": len(incoming),
        "valid_records": len(valid),
        "new_records": len(new_records),
        "invalid_records": invalid_count,
        "total_records": len(combined),
        "unique_npns": int(combined.npn_number.nunique()),
        "unique_urls": int(norm_url(combined.profile_page_url).nunique()),
        "completed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    temp = CHECKPOINT.with_suffix(".tmp")
    temp.write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")
    os.replace(temp, CHECKPOINT)

    elapsed = time.perf_counter() - start

    print("\nPROCESSING COMPLETE")
    print("VALID NEW RECORDS:", len(new_records))
    print("INVALID RECORDS:", invalid_count)
    print("TOTAL RECORDS:", len(combined))
    print("UNIQUE NPNs:", combined.npn_number.nunique())
    print("UNIQUE URLs:", norm_url(combined.profile_page_url).nunique())
    print("ELAPSED SECONDS:", round(elapsed, 2))
    print("OUTPUT:", OUTPUT.resolve())
    print("CHECKPOINT:", CHECKPOINT.resolve())
    print("AUDIT: PASSED")

if __name__ == "__main__":
    main()
