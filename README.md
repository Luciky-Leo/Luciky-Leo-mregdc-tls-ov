# MregDC-TLS ovarian cancer reproducibility package

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20523737.svg)](https://doi.org/10.5281/zenodo.20523737)

This repository contains reviewer-facing code, source-data tables, and compact figure files for the manuscript:

**Spatial association of TLS programs and LAMP3+CCR7+ mregDC states marks an immune-prognostic context in ovarian cancer**

Target journal: *Journal of Translational Medicine*.

## Repository scope

This repository is intended to support peer review and archival code availability. It is available at:

https://github.com/Luciky-Leo/Luciky-Leo-mregdc-tls-ov

It contains:

- `code/`: package-building, figure-compression, TCGA-OV clinical-covariate retrieval, adjusted Cox sensitivity analysis, and Supplementary Table S3 accession scripts.
- `source_data/`: current-numbering source-data folders for Fig. 1-Fig. 11 and Supplementary Figures S1-S6.
- `source_data/SOURCE_DATA_INDEX.csv`: primary figure-to-source-data map. Use this file first.
- `manuscript/`: LaTeX source files needed to compile the review-upload manuscript.
- `figures_for_review/`: compressed review/upload figure PDFs.
- `supplementary/`: supplementary information source/PDF, supplementary figures, and supplementary tables.

Large raw public datasets are not redistributed here. Dataset identifiers, URLs, and version notes are provided in:

- `source_data/Tables_signature_and_GEO/Supplementary_Table_S3_spatial_and_10x_dataset_accessions.xlsx`
- `source_data/SOURCE_DATA_INDEX.csv`

## Main limitations

The manuscript uses public single-cell, spatial transcriptomic, TCGA/GTEx, virtual perturbation, and docking-prioritization analyses. The IF layer is representative image-based support based on flattened merged images, and the manuscript does not use those images to claim tissue-level cell density or abundance. Spatial HLA-family evidence is treated as antigen-presentation/MHC-II proxy evidence where exact HLA genes are absent from public spatial matrices.

## Quick file map

| Item | Location |
|---|---|
| Source-data index | `source_data/SOURCE_DATA_INDEX.csv` |
| Code inventory | `code/CODE_INVENTORY_FOR_REVIEW.csv` |
| Manuscript LaTeX | `manuscript/manuscript_jtm_springer_nature_review_upload.tex` |
| Review figures | `figures_for_review/Fig1.pdf` through `Fig11.pdf` |
| Supplementary information | `supplementary/Supplementary_Information_jtm_springer_nature.pdf` |
| Dataset accession table | `source_data/Tables_signature_and_GEO/Supplementary_Table_S3_spatial_and_10x_dataset_accessions.xlsx` |

## Reproducibility notes

The local analysis environment used for final package assembly followed the E-drive research environment policy:

- general Python work: `research-py312`
- R/statistical work: `research-r45`
- heavy bioinformatics compatibility: `bioinfo-py311-r45`

A minimal portable environment specification is provided in `environment.yml`. Some upstream analyses relied on method-specific local environments and public datasets that must be re-downloaded from the accessions listed in Supplementary Table S3.

## Suggested citation

This repository is archived at Zenodo under DOI:

https://doi.org/10.5281/zenodo.20523737

Cite the archived release together with the final published article.


