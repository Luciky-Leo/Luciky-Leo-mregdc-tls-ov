# Source Data Current Numbering

This folder provides a current-numbering entry point for the submitted Journal of Translational Medicine manuscript.

The legacy source-data folders are retained for traceability because several files were generated before the final figure renumbering. Reviewers should start from `SOURCE_DATA_INDEX.csv`, which maps the submitted Fig. 1-Fig. 11 and Supplementary Fig. S1-S6 to the current source-data folders.

Important interpretation notes:

- Fig. 3 IF values are raw illustrative ROI counts from one representative case and one ROI per cancer type. They should not be used as per-mm2 tissue densities, single-cell four-marker co-localization statistics, or cross-cancer abundance estimates.
- Spatial antigen-presentation measurements in public Xenium/scFFPE analyses are MHC-II/AP proxy signals when direct HLA-DRA/HLA genes are unavailable.
- Survival and model-validation source data are internal TCGA-OV analyses and do not represent external clinical validation. A GDC clinical sensitivity Cox model adjusted for age, advanced FIGO stage, and high grade is included under current Fig. 9; residual disease was not modeled because only 14 of 426 model patients had recorded values.
- Fig. 2 source tables currently cover marker and feature matrices; CellChat and pseudotime panel-level tables should be extracted from the original single-cell workflow if a complete source-data archive is required before upload.
- Supplementary Table S3 lists the 23 public multi-sample spatial samples and the public 10x Visium, scFFPE, and Xenium Prime ovarian cancer dataset URLs/version notes.
- Code/source-data packaging is reviewer-facing. A public repository and archival DOI remain the preferred final code-availability solution.
