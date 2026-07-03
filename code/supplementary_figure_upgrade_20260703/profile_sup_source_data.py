#!/usr/bin/env python3
"""Profile supplementary source-data tables for the CNS redraw v2 pass."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT = Path("/mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629")
SOURCE = PROJECT / "07_submission_package_R1/_source_data_stage"
OUT = PROJECT / "09_SUP_CNS_redraw_v2_20260703/source_profile"


SUP_FILES = {
    "S1_haystack_ranked": "FigS01_singleCellHaystack_audit/SourceData_FigS1_singleCellHaystack_ranked_features.tsv",
    "S1_haystack_manifest": "FigS01_singleCellHaystack_audit/SourceData_FigS1_input_manifest.tsv",
    "S1_haystack_qc": "FigS01_singleCellHaystack_audit/SourceData_FigS1_run_qc.tsv",
    "S2_hotspot_ranked": "FigS02_Hotspot_audit/SourceData_FigS2_Hotspot_autocorrelations.tsv",
    "S2_hotspot_input_qc": "FigS02_Hotspot_audit/SourceData_FigS2_input_qc.tsv",
    "S2_hotspot_run_qc": "FigS02_Hotspot_audit/SourceData_FigS2_run_qc.tsv",
    "S4_spot_scores": "FigS04_multi_sample_spatial_source/multi_sample_spatial_extended_selected_map_spot_scores.csv",
    "S4_marker_maps": "FigS04_multi_sample_spatial_source/multi_sample_spatial_extended_selected_marker_expression_maps.csv",
    "S4_sample_metrics": "FigS04_multi_sample_spatial_source/multi_sample_spatial_extended_sample_metrics_long.csv",
    "S4_dataset_summary": "FigS04_multi_sample_spatial_source/multi_sample_spatial_extended_dataset_metric_summary.csv",
    "S4_gene_coverage": "FigS04_multi_sample_spatial_source/multi_sample_spatial_extended_gene_coverage_fraction.csv",
    "S5_cv": "FigS05_model_validation/source_LASSO_CV_curve.csv",
    "S5_coef": "FigS05_model_validation/source_LASSO_lambda_min_coefficients.csv",
    "S5_auc": "FigS05_model_validation/source_time_dependent_ROC_AUC.csv",
    "S5_roc": "FigS05_model_validation/source_time_dependent_ROC_curve.csv",
    "S5_calibration": "FigS05_model_validation/source_calibration_by_quintile.csv",
    "S5_patients": "FigS05_model_validation/source_model_input_patients.csv",
    "S6_partial": "FigS06_specificity_adjustment/partial_correlation_results_combined.csv",
    "S6_controls": "FigS06_specificity_adjustment/immune_control_definitions.csv",
    "S6_plot_values": "FigS06_specificity_adjustment/specificity_compact_plot_values.csv",
    "S6_regression": "FigS06_specificity_adjustment/tcga_adjusted_regression_results.csv",
    "S7_matrix": "FigS07_drug_prioritization_docking/FigS07_CH_drug_vulnerability_matrix_source_matrix.csv",
    "S7_scores": "FigS07_drug_prioritization_docking/FigS07_drug_prioritization_derived_scores.tsv",
}


def read_table(path: Path) -> pd.DataFrame:
    sep = "\t" if path.suffix.lower() in {".tsv", ".txt"} else ","
    return pd.read_csv(path, sep=sep)


def numeric_summary(df: pd.DataFrame) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for col in df.select_dtypes(include="number").columns:
        s = df[col].dropna()
        if s.empty:
            continue
        out[col] = {
            "min": float(s.min()),
            "p25": float(s.quantile(0.25)),
            "median": float(s.median()),
            "p75": float(s.quantile(0.75)),
            "max": float(s.max()),
        }
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    samples = {}
    for key, rel in SUP_FILES.items():
        path = SOURCE / rel
        df = read_table(path)
        records.append(
            {
                "key": key,
                "relative_path": rel,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": ";".join(df.columns.astype(str)),
            }
        )
        samples[key] = {
            "relative_path": rel,
            "head": df.head(8).to_dict(orient="records"),
            "numeric_summary": numeric_summary(df),
        }
    pd.DataFrame(records).to_csv(OUT / "supp_source_table_profile.csv", index=False)
    with (OUT / "supp_source_table_samples.json").open("w", encoding="utf-8") as handle:
        json.dump(samples, handle, indent=2, ensure_ascii=False)

    # Spatial map metadata used by the redraw script.
    spot = read_table(SOURCE / SUP_FILES["S4_spot_scores"])
    spatial_meta = (
        spot.groupby(["dataset", "sample_id", "sample_panel"], dropna=False)
        .agg(
            n_spots=("spot", "count"),
            x_min=("x", "min"),
            x_max=("x", "max"),
            y_min=("y", "min"),
            y_max=("y", "max"),
            tls_high_fraction=("TLS_high", "mean"),
            mregdc_high_fraction=("mregDC_high", "mean"),
            cohigh_fraction=("TLS_mregDC_cohigh", "mean"),
        )
        .reset_index()
        .sort_values(["dataset", "sample_id"])
    )
    spatial_meta.to_csv(OUT / "spatial_sample_profile.csv", index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
