# MregDC-TLS ovarian cancer code and source-data package

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21026437.svg)](https://doi.org/10.5281/zenodo.21026437)

This repository contains reviewer-facing code, source-data tables, manuscript
source files, and compact figure files for the Cancers submission version of the
manuscript:

**Integrative Single-Cell and Spatial Transcriptomic Analysis Identifies a
TLS-Associated LAMP3+CCR7+ mregDC Antigen-Presentation Program in Ovarian
Cancer**

Target journal: *Cancers*.

## Repository scope

This repository is intended to support peer review and archival code
availability. It is available at:

https://github.com/Luciky-Leo/Luciky-Leo-mregdc-tls-ov

It contains:

- `code/`: package-building, figure-compression, TCGA-OV clinical-covariate
  retrieval, adjusted Cox sensitivity analysis, and Supplementary Table S3
  accession scripts. For the R1 revision, this folder also includes a
  figure-panel-to-source-data map, a runnable validation script for every
  main figure panel group, and Fig. 1/Fig. 2 analysis scripts.
- `source_data/`: current-numbering source-data folders for Fig. 1-Fig. 10 and
  Supplementary Figures S1-S7.
- `source_data/SOURCE_DATA_INDEX.csv`: primary figure-to-source-data map. Use
  this file first.
- `manuscript/`: Cancers/MDPI LaTeX source, bibliography, MDPI support files,
  compiled PDF, and submission precheck report.
- `figures_for_review/`: review/upload figure PDFs for Fig. 1-Fig. 10.
- `supplementary/`: supplementary information PDF, supplementary figures, and
  supplementary tables. The R1 supplementary-figure production export archive
  includes PDF, SVG, and TIFF versions of Supplementary Figures S1-S7.

Large raw public datasets are not redistributed here. Dataset identifiers,
URLs, and version notes are provided in:

- `source_data/Tables_signature_and_GEO/Supplementary_Table_S3_spatial_and_10x_dataset_accessions.xlsx`
- `source_data/SOURCE_DATA_INDEX.csv`

## Main limitations

The manuscript uses public single-cell, spatial transcriptomic, TCGA/GTEx,
virtual perturbation, and docking-prioritization analyses. The IF layer is
representative image-based support based on flattened merged images, and the
manuscript does not use those images to claim tissue-level cell density or
abundance. Spatial HLA-family evidence is treated as antigen-presentation/MHC-II
proxy evidence where exact HLA genes are absent from public spatial matrices.
Virtual perturbation and drug-prioritization analyses are hypothesis-generating
and require experimental validation.

## Quick file map

| Item | Location |
|---|---|
| Source-data index | `source_data/SOURCE_DATA_INDEX.csv` |
| Code inventory | `code/CODE_INVENTORY_FOR_REVIEW.csv` |
| Main figure panel/source map | `code/figure_panel_script_source_map_repo.csv` |
| Main figure source validation script | `code/validate_main_figure_panel_sources.py` |
| Main figure source validation report | `code/output/panel_source_validation_report.csv` |
| Fig. 1 analysis script | `code/fig1_scRNA_reference.py` |
| Fig. 2 analysis script | `code/fig2_mregDC_program.py` |
| Supplementary figure redraw scripts | `code/supplementary_figure_upgrade_20260703/` |
| Supplementary figure QC reports | `docs/supplementary_figure_upgrade_20260703/` |
| R1 IF raw-channel availability audit | `docs/IF_CHANNEL_AVAILABILITY_AUDIT.md` |
| R1 added-analysis pre-specification | `docs/R1_ADDED_ANALYSIS_PRESPEC.md` |
| Cancers manuscript LaTeX | `manuscript/manuscript_cancers_mdpi.tex` |
| Cancers compiled PDF | `manuscript/manuscript_cancers_mdpi.pdf` |
| Review figures | `figures_for_review/Fig1.pdf` through `Fig10.pdf` |
| Supplementary information | `supplementary/Supplementary_Information.pdf` |
| Supplementary figure production exports | `supplementary/CNS_ready_supplementary_production_exports.zip` |
| Dataset accession table | `source_data/Tables_signature_and_GEO/Supplementary_Table_S3_spatial_and_10x_dataset_accessions.xlsx` |

## Code and source-data notes

The local analysis environment used for final package assembly followed the
E-drive research environment policy:

- general Python work: `research-py312`
- R/statistical work: `research-r45`
- heavy bioinformatics compatibility: `bioinfo-py311-r45`

A minimal portable environment specification is provided in `environment.yml`.
Some upstream analyses relied on method-specific local environments and public
datasets that must be re-downloaded from the accessions listed in Supplementary
Table S3.

The public code folder is scoped to reviewer-facing package construction and
sensitivity/source-data scripts. Full raw-data reruns may require public data
downloads and method-specific local environments as described in the manuscript
methods and source-data notes.

Fig. 1 and Fig. 2 include analysis scripts that generate the submitted cohort,
marker/program, and classifier-weight summaries from deposited source-data
tables.

To validate the R1 main figure panel/source-data map after downloading this
repository:

```bash
python code/validate_main_figure_panel_sources.py \
  --project-root . \
  --map code/figure_panel_script_source_map_repo.csv \
  --out code/output/panel_source_validation_report.csv
```

The expected validation output contains 46 source-file checks with status
`exists`.

## Suggested citation

This repository is archived at Zenodo under the concept DOI:

https://doi.org/10.5281/zenodo.21026437

Cite the archived release together with the final published article.
