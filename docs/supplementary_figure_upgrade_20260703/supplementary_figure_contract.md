# Supplementary Figure Contract

## Global Contract

- Scope: revised supplementary figures for the Cancers R1 response package.
- Figure width: 180 mm.
- Panel count: 4 panels per figure for S1-S14.
- Panel labels: A-D only.
- In-figure text discipline: no sentence-like explanatory subtitles; interpretation belongs in the Results, Discussion, response letter, or figure legends.
- Data rule: all panels are rendered from source tables in `07_submission_package_R1/_source_data_stage`; spatial panels use x/y coordinates and score columns, not screenshots.
- Export rule: PDF/SVG with editable text where possible plus PNG previews at 300 dpi.
- Claim boundary: IF panels support representative mregDC marker presence only; spatial antigen-presentation maps use an AP/MHC-II proxy when exact HLA genes are unavailable; drug and perturbation panels remain hypothesis-generating.

## Figure Map

### Supplementary Figure S1

One-sentence conclusion: singleCellHaystack detected a ranked set of non-random spatial genes with internally consistent evidence metrics.

- A: top singleCellHaystack evidence genes.
- B: D_KL versus statistical evidence concordance.
- C: top-gene metric matrix.
- D: ranked evidence decay.

### Supplementary Figure S2

One-sentence conclusion: Hotspot provides an independent spatial-autocorrelation audit and overlaps with singleCellHaystack at the ranked-gene level.

- A: top Hotspot autocorrelation genes.
- B: Hotspot C versus Z evidence concordance.
- C: ranked-method overlap.
- D: shared-gene method comparison matrix.

### Supplementary Figure S3

One-sentence conclusion: source-data spatial maps support a TLS/mregDC/AP-proxy spatial niche in a representative high-support spatial sample.

- A: TLS integrated score map.
- B: mregDC score map.
- C: AP/MHC-II proxy score map.
- D: TLS/mregDC co-high overlay with smoothed score-field contours.

### Supplementary Figure S4

One-sentence conclusion: the spatial niche signal is reproducible across public spatial-transcriptomic datasets and remains interpretable despite panel-level gene-coverage differences.

- A: multi-sample co-high spatial overlays.
- B: dataset-level spatial metric heatmap.
- C: sample-level co-high observed/expected distribution.
- D: gene-coverage fraction heatmap.

### Supplementary Figure S5

One-sentence conclusion: the patient-level prognostic model is shown with its regularization, coefficients, time-dependent ROC, and calibration behavior.

- A: LASSO cross-validation curve.
- B: non-zero coefficient lollipop plot.
- C: time-dependent ROC curves.
- D: calibration by predicted-risk quintile.

### Supplementary Figure S6

One-sentence conclusion: mregDC/TLS and mregDC/AP associations retain measurable but bounded signal after immune-context and lineage controls.

- A: raw versus partial correlation comparison.
- B: adjusted-correlation matrix.
- C: adjusted regression coefficient forest plot.
- D: model-control/sample-size summary.

### Supplementary Figure S7

One-sentence conclusion: the drug-prioritization layer is presented as a hypothesis-generating computational screen with transparent evidence dimensions.

- A: drug evidence-dimension matrix.
- B: integrated priority ranking.
- C: target evidence versus program-reversal support.
- D: priority distribution by target class.

### Supplementary Figure S8

One-sentence conclusion: the scRNA-seq and representative IF source layers support the existence of an mregDC marker program across gynecologic cancer contexts without overusing IF as tissue-level quantification.

- A: disease/sample support in the scRNA-seq reference.
- B: marker weights for the mregDC/AP program.
- C: marker-score source summary.
- D: representative IF raw count summary.

### Supplementary Figure S9

One-sentence conclusion: Xenium spatial maps show the same coordinate framework for TLS, mregDC, AP/MHC-II proxy, and IFN-response programs.

- A: TLS integrated map.
- B: mregDC program map.
- C: AP/MHC-II proxy map.
- D: IFN-response map.

### Supplementary Figure S10

One-sentence conclusion: TLS-field segmentation and field-level summaries define spatial objects that can be linked to co-highness and panel gene coverage.

- A: TLS-field grid components with co-high cells.
- B: field size versus co-high fraction.
- C: co-high field program matrix.
- D: Xenium panel gene-coverage summary.

### Supplementary Figure S11

One-sentence conclusion: TLS-associated programs vary along distance and score-gradient axes, supporting spatial organization rather than only sample-level abundance.

- A: Xenium distance gradients from TLS fields.
- B: multi-sample TLS-decile program trends.
- C: co-high fraction by TLS decile.
- D: decile readout matrix.

### Supplementary Figure S12

One-sentence conclusion: ten immune-deconvolution methods place the mregDC/TLS signal within a broader immune-rich context while exposing method-level heterogeneity.

- A: ten-method run status.
- B: immune-method atlas heatmap.
- C: method-level IF-association summary.
- D: immune-class summary.

### Supplementary Figure S13

One-sentence conclusion: patient-level composite features and risk groups provide a compact bridge between spatial programs and prognosis modeling.

- A: patient-feature atlas subset.
- B: risk-group score shifts.
- C: risk-score distribution.
- D: patient-level correlation matrix.

### Supplementary Figure S14

One-sentence conclusion: virtual perturbation analyses prioritize regulatory targets at the TF/program level and should be interpreted as computational vulnerability hypotheses.

- A: virtual perturbation matrix.
- B: CellOracle TF deltas.
- C: target-gene shifts.
- D: target-shift burden.
