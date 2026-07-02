# CNS-Level Supplementary Figure Audit

Project: Cancers R1 revision, mregDC/TLS ovarian cancer manuscript  
Audit date: 2026-07-03  
Scope: Supplementary Figures S1-S7 after supplementary figure redraw and package synchronization

## Audit Standard

This audit applies a conservative Nature/CNS-style figure standard to supplementary figures:

- Each supplementary figure must answer a distinct reviewer-facing question.
- Each figure must have a bounded claim and not introduce unsupported biological conclusions.
- Final production exports should include fixed-width PDF, editable SVG, and high-resolution TIFF where feasible.
- Quantitative panels must be traceable to staged source-data tables.
- Image/map panels must state whether they are source-data rerenders or layout redraws from existing image/PDF layers.
- Upload-facing files must be synchronized with `latex_source_clean`, `Source_Data.zip`, and `Cancers_R1_Supplementary_Files.zip`.

The technical export target used here is a 180 mm-wide double-column-style canvas, with journal-ready PDF/SVG/TIFF exports. This follows the same conservative visual-production logic used by current Nature figure guidance: editable vector line art where possible, high-resolution raster exports when needed, and restrained typography/legends.

## Figure Contract Summary

| Figure | Core reviewer-facing question | Evidence role | Current verdict |
|---|---|---|---|
| S1 | Do singleCellHaystack-ranked genes show spatial non-randomness relevant to TLS/mregDC biology? | Spatial feature audit | Pass |
| S2 | Do Hotspot-ranked genes show spatial autocorrelation and overlap with TLS/mregDC/AP marker sets? | Independent spatial feature audit | Pass |
| S3 | Where do the Xenium spatial modules, co-high cells, and high-ranking audit genes map in tissue coordinates? | Spatial map support | Pass with boundary note |
| S4 | Are the spatial programs and marker/gene coverage supported across public spatial datasets? | Multi-sample robustness/support | Pass |
| S5 | Are the prognostic model outputs internally checked with ROC, LASSO-Cox CV, and calibration? | Model-validation supplement | Pass |
| S6 | Are the main TLS/mregDC associations robust to immune-richness/specificity adjustment? | Specificity/sensitivity audit | Pass |
| S7 | Does the exploratory drug layer summarize computational prioritization without implying efficacy? | Hypothesis-generating supplement | Pass with boundary note |

## Format Audit

Source file: `SUPPLEMENTARY_FIGURE_FORMAT_AUDIT_20260703.csv`

| Figure | Width | Height | PDF | SVG | TIFF | Upload-facing file |
|---|---:|---:|---|---|---|---|
| S1 | 180.0 mm | 78.0 mm | yes | yes | yes | `FigureS1_singleCellHaystack.png` |
| S2 | 180.0 mm | 78.0 mm | yes | yes | yes | `FigureS2_Hotspot.png` |
| S3 | 180.0 mm | 188.0 mm | yes | yes | yes | `FigureS3_Xenium_spatial_maps-re.pdf` |
| S4 | 180.0 mm | 105.0 mm | yes | yes | yes | `FigureS4_multi_sample_spatial_validation.png` |
| S5 | 180.0 mm | 75.0 mm | yes | yes | yes | `FigureS5_model_validation.png` |
| S6 | 180.0 mm | 62.0 mm | yes | yes | yes | `FigureS6_specificity_adjusted_associations.png` |
| S7 | 179.9 mm | 145.0 mm | yes | yes | yes | `Supplementary_Figure_S7_drug_prioritization.pdf` |

## Figure-by-Figure Assessment

### Supplementary Figure S1

Verdict: pass.

The redrawn figure now works as a compact two-panel audit rather than a loose ranked list. Panel A shows the highest singleCellHaystack evidence genes; panel B explicitly audits TLS/mregDC/AP marker overlap. This makes the figure's purpose clear: it supports spatial non-randomness and marker relevance, not a new cell-state discovery claim.

Remaining boundary: this is an audit of spatial non-randomness in the available Xenium subset. It should not be phrased as independent validation of histological TLS maturity.

### Supplementary Figure S2

Verdict: pass.

S2 mirrors S1 using Hotspot spatial-autocorrelation evidence. This paired structure is stronger than the earlier heterogeneous look because S1 and S2 now act as two method-parallel audits. The marker-audit panel makes the method output biologically interpretable without overstating causality.

Remaining boundary: Hotspot evidence supports spatial autocorrelation, not lineage causality.

### Supplementary Figure S3

Verdict: pass with boundary note.

S3 was layout-redrawn into a unified spatial-map page with aligned typography, shared colorbars, and compact panel hierarchy. This is visually much closer to a high-impact supplementary spatial map. The redraw uses the prior S3 spatial-map PDF as a source layer and does not introduce new spatial computations.

Required interpretation language: describe S3 as descriptive spatial-map support for Xenium feature audits and co-high cell visualization. Do not describe it as a new spatial segmentation result or a new statistical test.

### Supplementary Figure S4

Verdict: pass.

S4 now has a clear three-panel logic: dataset-level support, signature-gene coverage, and exact-marker coverage. This directly addresses reviewer concerns about multi-sample support and missing HLA-class-II marker coverage. The figure is no longer a generic heatmap.

Remaining boundary: HLA-DRA availability and AP/MHC-II proxy coverage must remain framed as panel-dependent and proxy-based.

### Supplementary Figure S5

Verdict: pass.

S5 now supports model validity in a standard way: ROC, LASSO-Cox CV, and calibration. This is the correct supplement-level location for technical prognostic-model checks. It should remain supplementary rather than main because the survival model is internal and exploratory.

Remaining boundary: do not imply external prognostic validation.

### Supplementary Figure S6

Verdict: pass.

S6 now shows raw vs adjusted associations across TCGA-OV patients, spatial spots, and Xenium cells using a compact aligned correlation format. It is useful because it makes the negative/attenuated Xenium adjustment visible rather than hiding it.

Remaining boundary: the adjusted Xenium result should be interpreted as a specificity/sensitivity check, not as failure of the whole spatial model.

### Supplementary Figure S7

Verdict: pass with boundary note.

S7 is now appropriately demoted from the main figure layer and presented as an exploratory drug-prioritization supplement. The four-panel structure separates evidence matrix, integrated priority, docking support, and target-class summary. This reduces reviewer risk compared with keeping drug screening in the main manuscript.

Required interpretation language: computational prioritization only; no therapeutic efficacy, no approved-treatment claim, no PIK3CA-response claim, and no experimentally confirmed reversal of mregDC/TLS phenotypes.

## Package Synchronization Evidence

Current upload-facing packages:

- `07_submission_package_R1/Cancers_R1_Supplementary_Files.zip`
- `07_submission_package_R1/Cancers_R1_LaTeX_Source.zip`
- `07_submission_package_R1/Source_Data.zip`

Current production export package:

- `08_supplementary_figure_upgrade_20260702/CNS_ready_supplementary_production_exports.zip`

Current visual overview:

- `08_supplementary_figure_upgrade_20260702/outputs/supplementary_redraw_contact_sheet.png`

Current precheck:

- `07_submission_package_R1/SUBMISSION_PRECHECK_REPORT.md`
- Status: `PASS`

## Residual Risks

1. The upgraded supplementary figures are stronger visually and technically, but they do not turn the project into a CNS-level experimental study. The main limitation remains reliance on public datasets and computational validation.
2. S3 is a layout redraw from a prior spatial-map source layer. This is acceptable for presentation but must not be described as a newly rerun analysis.
3. If the upgraded supplementary files are used for resubmission, the public GitHub/Zenodo reproducibility archive should be updated so the public package matches the submitted package.
4. If the editor requests individual figure uploads rather than a manuscript-embedded package, use the `production_exports` folder or the `CNS_ready_supplementary_production_exports.zip`.

## Final Audit Verdict

The supplementary figure set has reached a defensible high-impact-journal presentation standard for a computational/translational manuscript: each figure now has a clear role, staged source-data support, fixed-width exports, editable/high-resolution production files, and bounded interpretation language. No further supplementary-figure redrawing is required before resubmission unless the target journal or editor requests a different upload format.
