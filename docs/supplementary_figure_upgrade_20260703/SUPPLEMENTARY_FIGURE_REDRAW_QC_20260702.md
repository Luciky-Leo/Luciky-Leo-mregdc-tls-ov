# Supplementary Figure Redraw QC

Project: Cancers R1 revision, mregDC/TLS ovarian cancer manuscript  
Date: 2026-07-02  
Scope: Supplementary Figures S1-S7 and related upload files

## Rationale

The supplementary figures were upgraded because several panels looked like loose intermediate outputs rather than journal-ready supporting evidence. The redraw focused on improving scientific hierarchy, source-data traceability, and visual consistency while avoiding unsupported new biological claims.

## Figure-Level Actions

| Supplementary figure | Action | Rationale | Current upload file |
|---|---|---|---|
| S1 | Redrawn | Converted singleCellHaystack output into a two-panel non-randomness audit: ranked genes plus TLS/mregDC marker audit. | `FigureS1_singleCellHaystack.png` |
| S2 | Redrawn | Converted Hotspot output into a two-panel spatial-autocorrelation audit with the same grammar as S1. | `FigureS2_Hotspot.png` |
| S3 | Layout-redrawn | Rebuilt the Xenium spatial-map page from the existing S3 spatial-map PDF source layer to harmonize typography, panel spacing, and shared colorbar placement without adding new analysis. | `FigureS3_Xenium_spatial_maps-re.pdf` |
| S4 | Redrawn | Rebuilt multi-sample spatial validation as dataset-level support, signature-gene coverage, and exact-marker coverage. | `FigureS4_multi_sample_spatial_validation.png` |
| S5 | Redrawn | Rebuilt model validation as ROC, LASSO-Cox CV, and calibration panels with clearer labels and spacing. | `FigureS5_model_validation.png` |
| S6 | Redrawn | Rebuilt specificity/sensitivity associations as aligned forest-style correlation panels for TCGA-OV, spatial spots, and Xenium cells. | `FigureS6_specificity_adjusted_associations.png` |
| S7 | Redrawn | Replaced former main Fig. 11 drug layer with a restrained supplementary prioritization figure: evidence matrix, integrated priority, docking-support plot, and target-class summary. | `Supplementary_Figure_S7_drug_prioritization.pdf` |

## Source Data and Reproducibility

- The redraw scripts are stored in:
  - `08_supplementary_figure_upgrade_20260702/scripts/redraw_supplementary_s1_s6.py`
  - `08_supplementary_figure_upgrade_20260702/scripts/redraw_s3_spatial_maps_layout.py`
  - `08_supplementary_figure_upgrade_20260702/scripts/redraw_s7_drug_prioritization.R`
  - `08_supplementary_figure_upgrade_20260702/scripts/make_redraw_contact_sheet.py`
- The S7 derived score table was generated and staged as:
  - `07_submission_package_R1/_source_data_stage/FigS07_drug_prioritization_docking/FigS07_drug_prioritization_derived_scores.tsv`
- The S3 layout-redrawn PDF/SVG/PNG were staged as:
  - `07_submission_package_R1/_source_data_stage/FigS03_Xenium_spatial_maps/FigureS3_Xenium_spatial_maps_redraw.pdf`
  - `07_submission_package_R1/_source_data_stage/FigS03_Xenium_spatial_maps/FigureS3_Xenium_spatial_maps_redraw.svg`
  - `07_submission_package_R1/_source_data_stage/FigS03_Xenium_spatial_maps/FigureS3_Xenium_spatial_maps_redraw.png`
- `SOURCE_DATA_INDEX.csv` was updated so FigS07 points to:
  - `FigS07_CH_drug_vulnerability_matrix_source_matrix.csv`
  - `FigS07_drug_prioritization_derived_scores.tsv`
- `SOURCE_DATA_INDEX.csv` was also updated so FigS03 points to the layout-redrawn files and the retained source screenshots/PDF.

## Package Synchronization

The following upload-facing files were rebuilt or synchronized:

- `07_submission_package_R1/Cancers_R1_Supplementary_Files.zip`
- `07_submission_package_R1/Cancers_R1_LaTeX_Source.zip`
- `07_submission_package_R1/Source_Data.zip`
- `07_submission_package_R1/Supplementary_Information.pdf`
- `07_submission_package_R1/latex_source_clean/Supplementary_Information.pdf`
- `07_submission_package_R1/latex_source_clean/manuscript_cancers_mdpi.tex`
- `08_supplementary_figure_upgrade_20260702/CNS_ready_supplementary_vector_exports.zip`
- `08_supplementary_figure_upgrade_20260702/CNS_ready_supplementary_production_exports.zip`

All S1-S7 production PDFs were regenerated on fixed-width 180 mm canvases, and each supplementary figure now has PDF, SVG, and TIFF exports in `08_supplementary_figure_upgrade_20260702/production_exports`.

The manuscript data-availability statement was updated from "Figs. 1--11 and Supplementary Figs. S1--S6" to "Figs. 1--10 and Supplementary Figs. S1--S7".

## Pre-Submission Check

Command:

```bash
wsl -d Ubuntu -- bash -lc "cd /mnt/e/Reserch && /mnt/e/WSL/micromamba/bin/micromamba run -n research-py312 python _env/scripts/check_submission_integrity.py --manuscript /mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629/07_submission_package_R1/latex_source_clean/manuscript_cancers_mdpi.tex --package /mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629/07_submission_package_R1/latex_source_clean --expected-figures 10 --expected-supp-figures 7 --expected-supp-tables 3 --skip-url-check --output /mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629/07_submission_package_R1/SUBMISSION_PRECHECK_REPORT.md --json-output /mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629/07_submission_package_R1/SUBMISSION_PRECHECK_REPORT.json --no-fail-exit"
```

Result: `PASS`

Detected main figures: 10  
Detected supplementary figures: 7  
Detected supplementary tables: 3

## Residual Notes

1. The local machine currently has no available LaTeX compiler in PATH (`latexmk`, `pdflatex`, `xelatex`, and `tectonic` were not found), so the compiled main manuscript PDF was not regenerated locally after the Data Availability wording change.
2. The LaTeX source package is synchronized and should compile through the journal portal.
3. If this upgraded supplement set is used as the final resubmission package, the public GitHub/Zenodo release should be updated or clearly documented so the code/source-data archive matches the submitted package.
4. Supplementary Figure S3 was layout-redrawn from the existing spatial-map source layer; it should be described as a presentation/layout upgrade, not as a new spatial analysis.

## Overall QC Conclusion

The supplementary figure set is now more defensible: S1/S2 support spatial non-randomness, S3 provides spatial-map evidence in a harmonized layout, S4 supports multi-sample spatial validation, S5 supports prognostic model checks, S6 supports specificity/sensitivity analysis, and S7 supports hypothesis-generating drug prioritization without moving the drug layer into the main narrative.
