#!/usr/bin/env python3
"""Generate Fig. 2 mregDC source-data summaries.

This script regenerates reviewer-checkable marker, program, and
classifier-weight summaries from the deposited Fig. 2 source-data matrix.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


MARKERS = [
    "ITGAX",
    "LAMP3",
    "CCR7",
    "CD74",
    "B2M",
    "TAP1",
    "TAP2",
    "CIITA",
    "NLRC5",
    "PSMB8",
    "PSMB9",
    "CD40",
    "CD274",
    "CCL17",
    "CLEC9A",
    "CD1C",
]


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


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
        default="code/output/fig2_mregdc_program",
        help="Output directory relative to project root",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    src = root / "source_data" / "Fig02_scRNA_mregDC_program"
    outdir = root / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    header, rows = read_tsv(src / "scRNA_cell_marker_feature_matrix.tsv")
    _, weights = read_tsv(src / "scRNA_linear_SVM_marker_weights.tsv")
    marker_fields = [marker for marker in MARKERS if marker in header]

    n_cells = len(rows)
    if_core_values = [to_float(row.get("IF_core_score", "0")) for row in rows]
    if_core_high = [str(row.get("IF_core_high", "")).upper() == "TRUE" for row in rows]
    n_if_core_high = sum(if_core_high)

    marker_summary: list[dict[str, object]] = []
    for marker in marker_fields:
        values = [to_float(row.get(marker, "0")) for row in rows]
        high_values = [value for value, high in zip(values, if_core_high) if high]
        low_values = [value for value, high in zip(values, if_core_high) if not high]
        pct_expr = sum(value > 0 for value in values) / n_cells if n_cells else 0
        mean_all = sum(values) / n_cells if n_cells else 0
        mean_high = sum(high_values) / len(high_values) if high_values else 0
        mean_low = sum(low_values) / len(low_values) if low_values else 0
        marker_summary.append(
            {
                "marker": marker,
                "mean_all": round(mean_all, 6),
                "pct_expressing": round(pct_expr, 6),
                "mean_IF_core_high": round(mean_high, 6),
                "mean_IF_core_not_high": round(mean_low, 6),
                "mean_difference_high_minus_not_high": round(mean_high - mean_low, 6),
            }
        )

    marker_summary.sort(key=lambda row: float(row["mean_difference_high_minus_not_high"]), reverse=True)
    write_csv(
        outdir / "Fig2_marker_summary.csv",
        marker_summary,
        [
            "marker",
            "mean_all",
            "pct_expressing",
            "mean_IF_core_high",
            "mean_IF_core_not_high",
            "mean_difference_high_minus_not_high",
        ],
    )

    svm_rows = []
    for row in weights:
        clean = {key: row[key] for key in row}
        if "weight" in clean:
            clean["abs_weight"] = abs(to_float(clean["weight"]))
        svm_rows.append(clean)
    if svm_rows and "abs_weight" in svm_rows[0]:
        svm_rows.sort(key=lambda row: float(row["abs_weight"]), reverse=True)
    write_csv(outdir / "Fig2_svm_marker_weights.csv", svm_rows, list(svm_rows[0]) if svm_rows else [])

    summary = {
        "script_scope": "generates submitted Fig. 2 marker/program summaries from deposited source data",
        "n_cells": n_cells,
        "n_IF_core_high_cells": n_if_core_high,
        "fraction_IF_core_high": round(n_if_core_high / n_cells, 6) if n_cells else 0,
        "marker_fields_available": marker_fields,
        "top_markers_by_IF_core_difference": [
            row["marker"] for row in marker_summary[:5]
        ],
        "input_files": [
            "source_data/Fig02_scRNA_mregDC_program/scRNA_cell_marker_feature_matrix.tsv",
            "source_data/Fig02_scRNA_mregDC_program/scRNA_linear_SVM_marker_weights.tsv",
        ],
    }
    with (outdir / "Fig2_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(f"Wrote Fig. 2 source-data summaries to {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
