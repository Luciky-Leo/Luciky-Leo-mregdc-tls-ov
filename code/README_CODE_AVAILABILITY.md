# Code availability for peer review

This folder contains reviewer-facing scripts used for manuscript assembly, figure compression, dataset-accession table generation, and clinical sensitivity modeling for the Journal of Translational Medicine/Springer Nature submission package.

Reviewer-facing code provenance is summarized in `CODE_INVENTORY_FOR_REVIEW.csv`.

The current repository includes the manuscript-build and figure-compression scripts, the TCGA-OV GDC clinical-covariate fetch script, the adjusted Cox sensitivity script, and the Supplementary Table S3 dataset-accession script. Figure-level source-data files are provided under `../source_data/` and mapped to current manuscript figure numbers in `../source_data/SOURCE_DATA_INDEX.csv`.

Important limitation: large raw public single-cell and spatial datasets are not redistributed in this repository. Public dataset identifiers, URLs, and version notes are provided in Supplementary Table S3.
