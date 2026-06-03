#!/usr/bin/env python3
"""Create Supplementary Table S3 with public spatial and 10x dataset accessions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path("/mnt/e/Reserch/MregDC/JTM_SpringerNature_submission_20260602")
INFILE = ROOT / "source_data/Fig05_multi_sample_spatial_coupling/multi_sample_spatial_extended_sample_metrics_long.csv"
OUT_DIR = ROOT / "source_data/Tables_signature_and_GEO"
OUT_CSV = OUT_DIR / "Supplementary_Table_S3_spatial_and_10x_dataset_accessions.csv"
OUT_XLSX = OUT_DIR / "Supplementary_Table_S3_spatial_and_10x_dataset_accessions.xlsx"


TENX_URLS = {
    "10x_human_ovarian_cancer_ffpe_visium": "https://www.10xgenomics.com/datasets/human-ovarian-cancer-1-standard",
    "10x_scFFPE_17k_human_ovarian_cancer": "https://www.10xgenomics.com/datasets/17k-human-ovarian-cancer-scFFPE",
    "10x_xenium_prime_ffpe_human_ovarian_cancer": "https://www.10xgenomics.com/datasets/xenium-prime-ffpe-human-ovarian-cancer",
}


def geo_url(acc: str) -> str:
    return f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={acc}"


def main() -> None:
    x = pd.read_csv(INFILE)
    samples = (
        x[["dataset", "dataset_label", "sample_id", "sample_short", "n_spots"]]
        .drop_duplicates()
        .sort_values(["dataset", "sample_id"])
        .reset_index(drop=True)
    )
    rows = []
    for _, r in samples.iterrows():
        dataset = str(r["dataset"])
        sample_id = str(r["sample_id"])
        is_geo = dataset.startswith("GSE")
        is_gsm = sample_id.startswith("GSM")
        rows.append(
            {
                "table_role": "multi_sample_spatial_23_sample_analysis",
                "dataset_accession_or_id": dataset,
                "dataset_label": r["dataset_label"],
                "sample_accession_or_id": sample_id,
                "sample_short": r["sample_short"],
                "n_spots_or_cells": int(r["n_spots"]),
                "platform_or_assay": "public ovarian spatial transcriptomics",
                "software_or_analysis_version": "harmonized downstream scoring in this study",
                "dataset_url": geo_url(dataset) if is_geo else TENX_URLS.get(dataset, ""),
                "sample_url": geo_url(sample_id) if is_gsm else TENX_URLS.get(dataset, ""),
                "notes": "Included in the 23-sample, 56,546-spot multi-sample spatial support analysis.",
            }
        )

    rows.extend(
        [
            {
                "table_role": "10x_single_cell_reference_for_marker_workflow_and_scTenifoldKnk",
                "dataset_accession_or_id": "10x_scFFPE_17k_human_ovarian_cancer",
                "dataset_label": "Human Ovarian Cancer FFPE Single Cell Gene Expression Flex (Next GEM)",
                "sample_accession_or_id": "10x_scFFPE_17k_human_ovarian_cancer",
                "sample_short": "10x scFFPE",
                "n_spots_or_cells": 17553,
                "platform_or_assay": "Single Cell Gene Expression Flex, FFPE",
                "software_or_analysis_version": "Cell Ranger 8.0.1; GRCh38-2020-A",
                "dataset_url": TENX_URLS["10x_scFFPE_17k_human_ovarian_cancer"],
                "sample_url": TENX_URLS["10x_scFFPE_17k_human_ovarian_cancer"],
                "notes": "Used for public scFFPE marker workflow and virtual knockout/proxy analyses.",
            },
            {
                "table_role": "10x_xenium_spatial_exemplar",
                "dataset_accession_or_id": "10x_xenium_prime_ffpe_human_ovarian_cancer",
                "dataset_label": "FFPE Human Ovarian Cancer with 5K Human Pan Tissue and Pathways Panel plus 100 Custom Genes",
                "sample_accession_or_id": "Xenium_Prime_Ovarian_Cancer_FFPE_XRrun",
                "sample_short": "Xenium Prime OVC",
                "n_spots_or_cells": 407124,
                "platform_or_assay": "Xenium Prime 5K In Situ Gene Expression with Cell Segmentation, FFPE",
                "software_or_analysis_version": "Xenium Onboard Analysis 3.0.0; reanalyzed to XOA v3.2 formats using Xenium Ranger v3.1 relabel",
                "dataset_url": TENX_URLS["10x_xenium_prime_ffpe_human_ovarian_cancer"],
                "sample_url": TENX_URLS["10x_xenium_prime_ffpe_human_ovarian_cancer"],
                "notes": "Used as the public OVC Xenium exemplar for cell-level spatial segmentation and feature audits.",
            },
        ]
    )

    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False)
    try:
        out.to_excel(OUT_XLSX, index=False)
    except Exception as exc:  # pragma: no cover - depends on optional openpyxl
        print(f"XLSX export skipped: {exc}")
    print(f"Wrote {OUT_CSV}")
    if OUT_XLSX.exists():
        print(f"Wrote {OUT_XLSX}")


if __name__ == "__main__":
    main()
