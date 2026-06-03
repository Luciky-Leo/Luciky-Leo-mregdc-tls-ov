#!/usr/bin/env python3
"""Fetch TCGA-OV clinical covariates from the GDC cases API.

This script creates a reviewer-facing clinical covariate table for the
exploratory Cox sensitivity analysis. It does not modify the primary model.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd


ROOT = Path("/mnt/e/Reserch/MregDC/JTM_SpringerNature_submission_20260602")
MODEL_PATH = ROOT / "source_data/Fig09_LASSO_Cox_internal_validation/source_model_input_patients.csv"
OUT_PATH = ROOT / "source_data/Fig09_LASSO_Cox_internal_validation/tcga_ov_gdc_clinical_covariates.csv"
MERGED_OUT_PATH = ROOT / "source_data/Fig09_LASSO_Cox_internal_validation/source_model_input_patients_with_gdc_clinical.csv"
REPORT_PATH = ROOT / "source_data/Fig09_LASSO_Cox_internal_validation/tcga_ov_gdc_clinical_covariate_coverage.csv"


FIELDS = [
    "submitter_id",
    "demographic.age_at_index",
    "demographic.vital_status",
    "diagnoses.submitter_id",
    "diagnoses.age_at_diagnosis",
    "diagnoses.days_to_death",
    "diagnoses.days_to_last_follow_up",
    "diagnoses.primary_diagnosis",
    "diagnoses.tumor_stage",
    "diagnoses.tumor_grade",
    "diagnoses.figo_stage",
    "diagnoses.residual_disease",
    "diagnoses.year_of_diagnosis",
]


def fetch_cases() -> list[dict]:
    params = {
        "filters": json.dumps(
            {
                "op": "in",
                "content": {"field": "project.project_id", "value": ["TCGA-OV"]},
            }
        ),
        "fields": ",".join(FIELDS),
        "format": "JSON",
        "size": "2000",
    }
    url = "https://api.gdc.cancer.gov/cases?" + urlencode(params)
    with urlopen(url, timeout=60) as handle:
        payload = json.loads(handle.read().decode("utf-8"))
    return payload["data"]["hits"]


def first_diagnosis(case: dict) -> dict:
    diagnoses = case.get("diagnoses") or []
    if not diagnoses:
        return {}
    return sorted(diagnoses, key=lambda d: d.get("submitter_id", ""))[0]


def normalize_patient_id(x: str) -> str:
    x = str(x)
    parts = x.split("-")
    return "-".join(parts[:3]) if len(parts) >= 3 else x


def main() -> None:
    records = []
    for case in fetch_cases():
        diag = first_diagnosis(case)
        demo = case.get("demographic") or {}
        records.append(
            {
                "patient_id": normalize_patient_id(case.get("submitter_id", "")),
                "gdc_submitter_id": case.get("submitter_id", ""),
                "age_at_index_years": demo.get("age_at_index"),
                "age_at_diagnosis_days": diag.get("age_at_diagnosis"),
                "age_at_diagnosis_years": (
                    diag.get("age_at_diagnosis") / 365.25
                    if isinstance(diag.get("age_at_diagnosis"), (int, float))
                    else None
                ),
                "vital_status": demo.get("vital_status"),
                "primary_diagnosis": diag.get("primary_diagnosis"),
                "tumor_stage": diag.get("tumor_stage"),
                "tumor_grade": diag.get("tumor_grade"),
                "figo_stage": diag.get("figo_stage"),
                "residual_disease": diag.get("residual_disease"),
                "days_to_death": diag.get("days_to_death"),
                "days_to_last_follow_up": diag.get("days_to_last_follow_up"),
                "year_of_diagnosis": diag.get("year_of_diagnosis"),
            }
        )

    clinical = pd.DataFrame.from_records(records).drop_duplicates("patient_id")
    clinical.to_csv(OUT_PATH, index=False)

    model = pd.read_csv(MODEL_PATH)
    model["patient_id"] = model["patient_id"].map(normalize_patient_id)
    merged = model.merge(clinical, on="patient_id", how="left")
    merged.to_csv(MERGED_OUT_PATH, index=False)

    covariates = [
        "age_at_index_years",
        "age_at_diagnosis_years",
        "tumor_stage",
        "tumor_grade",
        "figo_stage",
        "residual_disease",
        "year_of_diagnosis",
    ]
    coverage = []
    for col in covariates:
        present = merged[col].notna() & (merged[col].astype(str).str.lower() != "not reported")
        coverage.append(
            {
                "covariate": col,
                "non_missing_n": int(present.sum()),
                "model_patients_n": int(len(merged)),
                "non_missing_fraction": float(present.mean()),
            }
        )
    pd.DataFrame(coverage).to_csv(REPORT_PATH, index=False)

    print(f"Wrote {OUT_PATH}")
    print(f"Wrote {MERGED_OUT_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
