# Code availability for peer review

This folder contains reviewer-facing scripts used for manuscript assembly,
figure compression, dataset-accession table generation, and clinical
sensitivity modeling. Some assembly scripts retain legacy JTM/Springer Nature
file names because they were created during earlier submission-package
preparation and are retained for provenance. The current manuscript, figure,
supplementary, and source-data files in this release correspond to the Cancers
submission version.

Reviewer-facing code provenance is summarized in `CODE_INVENTORY_FOR_REVIEW.csv`.

The current repository includes the manuscript-build and figure-compression
scripts, the TCGA-OV GDC clinical-covariate fetch script, the adjusted Cox
sensitivity script, and the Supplementary Table S3 dataset-accession script.
Figure-level source-data files are provided under `../source_data/` and mapped
to current manuscript figure numbers in `../source_data/SOURCE_DATA_INDEX.csv`.
Additional upstream analysis scripts used to derive the single-cell, spatial,
immune-deconvolution, perturbation, prognostic-model, and docking source tables
are available from the corresponding authors on reasonable request.

Important limitation: large raw public single-cell and spatial datasets are not redistributed in this repository. Public dataset identifiers, URLs, and version notes are provided in Supplementary Table S3.
