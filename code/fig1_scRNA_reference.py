#!/usr/bin/env python3
"""Generate Fig. 1 source-data summaries from deposited scRNA metadata.

This script regenerates the cohort and provenance summaries that support the
Fig. 1 study-design/scRNA-reference panels from deposited source data.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".", help="Repository root")
    parser.add_argument(
        "--outdir",
        default="code/output/fig1_scRNA_reference",
        help="Output directory relative to project root",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    src = root / "source_data" / "Fig01_study_design_scRNA_reference"
    outdir = root / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    manifest = read_csv(src / "Source_Data_Table_S1_scRNA_GEO_sample_manifest.csv")
    accession_summary = read_csv(src / "Source_Data_Table_S1_scRNA_GEO_accession_summary.csv")
    disease_summary = read_csv(src / "Source_Data_Table_S1_scRNA_GEO_disease_summary.csv")

    disease_counts = Counter(row["disease_group"] for row in manifest)
    accession_counts = Counter(row["dataset_accession"] for row in manifest)
    accession_by_disease: dict[str, Counter[str]] = defaultdict(Counter)
    for row in manifest:
        accession_by_disease[row["dataset_accession"]][row["disease_group"]] += 1

    disease_rows = [
        {"disease_group": disease, "n_samples": count}
        for disease, count in sorted(disease_counts.items())
    ]
    accession_rows = []
    for accession, count in sorted(accession_counts.items()):
        row: dict[str, object] = {"dataset_accession": accession, "n_samples": count}
        for disease in sorted(disease_counts):
            row[f"n_{disease.replace('/', '_')}"] = accession_by_disease[accession][disease]
        accession_rows.append(row)

    write_csv(
        outdir / "Fig1_disease_counts.csv",
        disease_rows,
        ["disease_group", "n_samples"],
    )

    accession_fields = ["dataset_accession", "n_samples"] + [
        f"n_{disease.replace('/', '_')}" for disease in sorted(disease_counts)
    ]
    write_csv(outdir / "Fig1_accession_counts.csv", accession_rows, accession_fields)
    write_csv(outdir / "Fig1_sample_manifest.csv", manifest, list(manifest[0]))

    summary = {
        "script_scope": "generates submitted Fig. 1 cohort and provenance summaries from deposited source data",
        "n_samples": len(manifest),
        "n_accessions": len(accession_counts),
        "disease_counts": dict(sorted(disease_counts.items())),
        "accession_counts": dict(sorted(accession_counts.items())),
        "input_files": [
            "source_data/Fig01_study_design_scRNA_reference/Source_Data_Table_S1_scRNA_GEO_sample_manifest.csv",
            "source_data/Fig01_study_design_scRNA_reference/Source_Data_Table_S1_scRNA_GEO_accession_summary.csv",
            "source_data/Fig01_study_design_scRNA_reference/Source_Data_Table_S1_scRNA_GEO_disease_summary.csv",
        ],
        "source_rows": {
            "sample_manifest": len(manifest),
            "accession_summary": len(accession_summary),
            "disease_summary": len(disease_summary),
        },
    }
    with (outdir / "Fig1_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(f"Wrote Fig. 1 source-data summaries to {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
