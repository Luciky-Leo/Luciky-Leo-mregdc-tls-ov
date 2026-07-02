# v1.1.3 - Supplementary figure production upgrade

This release updates the reviewer-facing reproducibility archive for the Cancers R1 revision after the supplementary-figure production pass.

## Main updates

- Synced the revised Cancers R1 manuscript source, compiled PDF, bibliography, and submission precheck report.
- Updated review/upload figures to the current main-figure set, Fig. 1-Fig. 10.
- Moved the exploratory drug-prioritization/docking material into Supplementary Figure S7 and removed the obsolete main Fig. 11 upload file.
- Rebuilt Supplementary Figures S1-S7 in a unified production style and added a production export archive containing PDF, SVG, and TIFF versions.
- Synced current source-data folders and `SOURCE_DATA_INDEX.csv` to the current numbering scheme, including `FigS07_drug_prioritization_docking`.
- Added the supplementary figure redraw scripts and QC reports under `code/supplementary_figure_upgrade_20260703/` and `docs/supplementary_figure_upgrade_20260703/`.

## Scope notes

- Supplementary Figure S3 is a layout and readability redraw from the existing spatial-map source layer, not a new spatial analysis.
- Supplementary Figure S7 remains an exploratory computational prioritization/docking analysis and does not claim drug efficacy or experimental therapeutic validation.
- The IF image layer remains representative merged-image support and is not used to claim tissue-level cell density or single-cell four-marker co-localization.

## Citation

Use the Zenodo concept DOI for the repository record:

https://doi.org/10.5281/zenodo.21026437

After GitHub release publication, Zenodo should mint a version-specific DOI for this release.
