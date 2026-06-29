#!/usr/bin/env python3
"""Validate main figure panel source-data links for the Cancers R1 revision.

This script is intentionally conservative. It does not claim to regenerate every
multi-panel publication PDF. It checks that each mapped main-figure panel has
reviewer-accessible source files and records compact file-level summaries.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def sniff_table(path: Path) -> tuple[int | None, int | None]:
    suffix = path.suffix.lower()
    if suffix not in {".csv", ".tsv", ".txt"}:
        return None, None
    delimiter = "\t" if suffix == ".tsv" else ","
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=delimiter)
            header = next(reader, [])
            rows = sum(1 for _ in reader)
        return rows, len(header)
    except UnicodeDecodeError:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
            reader = csv.reader(handle, delimiter=delimiter)
            header = next(reader, [])
            rows = sum(1 for _ in reader)
        return rows, len(header)


def summarize_json(path: Path) -> tuple[int | None, int | None]:
    if path.suffix.lower() != ".json":
        return None, None
    with path.open("r", encoding="utf-8") as handle:
        obj = json.load(handle)
    if isinstance(obj, dict):
        return len(obj), None
    if isinstance(obj, list):
        return len(obj), None
    return None, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".", help="Revision project root")
    parser.add_argument(
        "--map",
        default="04_analysis_scripts/figure_panel_script_source_map.csv",
        help="Panel-source mapping CSV relative to project root",
    )
    parser.add_argument(
        "--out",
        default="04_analysis_scripts/output/panel_source_validation_report.csv",
        help="Output CSV relative to project root",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    mapping = root / args.map
    out = root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    missing: list[str] = []
    with mapping.open("r", encoding="utf-8-sig", newline="") as handle:
        for record in csv.DictReader(handle):
            folder = root / record["source_folder"]
            for raw_name in record["source_files"].split(";"):
                name = raw_name.strip()
                if not name:
                    continue
                source = folder / name
                status = "exists" if source.exists() else "missing"
                if status == "missing":
                    missing.append(str(source))
                    file_size = ""
                    row_count = ""
                    col_count = ""
                else:
                    file_size = str(source.stat().st_size)
                    if source.suffix.lower() == ".json":
                        rc, cc = summarize_json(source)
                    else:
                        rc, cc = sniff_table(source)
                    row_count = "" if rc is None else str(rc)
                    col_count = "" if cc is None else str(cc)
                rows.append(
                    {
                        "figure": record["figure"],
                        "panel": record["panel"],
                        "claim_scope": record["claim_scope"],
                        "source_file": str(source.relative_to(root)),
                        "status": status,
                        "bytes": file_size,
                        "table_rows_or_json_items": row_count,
                        "table_columns": col_count,
                    }
                )

    fieldnames = [
        "figure",
        "panel",
        "claim_scope",
        "source_file",
        "status",
        "bytes",
        "table_rows_or_json_items",
        "table_columns",
    ]
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    if missing:
        print("Missing source files:")
        for item in missing:
            print(item)
        return 2
    print(f"Wrote {out} with {len(rows)} source-file checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

