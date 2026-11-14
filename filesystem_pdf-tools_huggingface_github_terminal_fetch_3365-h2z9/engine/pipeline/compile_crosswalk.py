"""Crosswalk compiler - reference implementation of the v3 release engine."""

import csv
import json


def compile_rows(register_entries, requests):
    """Build crosswalk rows from register entries and analyst requests."""
    rows = []
    for req in requests:
        match = None
        for entry in register_entries:
            if entry["title"] == req["entry_title"]:
                if req["locator_phrase"] in entry["scope"]:
                    match = entry
                    break
        if match is None:
            raise ValueError("unmatched request: %r" % req["entry_title"])
        rows.append({
            "filing_file": req["filing_file"],
            "entry_title": req["entry_title"],
            "locator_phrase": req["locator_phrase"],
            "entry_id": match["identifier"],
            "scope_quote": match["scope"],
        })
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


if __name__ == "__main__":
    print(json.dumps({"engine": "polygraph-harmonizer", "version": "3.0"}))
