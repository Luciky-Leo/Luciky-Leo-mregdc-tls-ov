# Cancers R1 added-analysis pre-specification

Date: 2026-06-29

Scope: only targeted mregDC-related analyses requested by reviewers. Do not rerun
the full pipeline or redraw the main figures unless these tests materially change
the claims.

## 1. IF raw-channel co-localization request

Reviewer request: perform formal co-localization statistics such as Pearson or
Manders using separated IF channels and expand ROI counts.

Gate A result: raw separated IF channel files were not found in the active
workspace, archived Cancers package, or staged source-data package.

Action:

- Do not calculate Pearson/Manders from merged JPG/PNG images.
- Revise text and response to state that formal channel-wise co-localization is not possible without raw separated channels.
- Keep Fig. 3 as representative tissue-image support with illustrative raw ROI counts only.

Fallback language:

"Because the available IF files for this revision were flattened merged images
rather than raw separated channel stacks, we did not perform Pearson/Manders
co-localization analyses. We revised the manuscript to describe the IF layer as
representative merged-image tissue support and removed density or single-cell
co-localization interpretations."

## 2. Inavolisib and PIK3CA status

Reviewer issue: inavolisib IC50 variation appears inconsistent with PIK3CA status
as a simple predictor.

Available current source data:

- `source_data/FigS07_drug_prioritization_docking/FigS07_CH_drug_vulnerability_matrix_source_matrix.csv`

Audit finding:

- The deposited Supplementary Fig. S7 source matrix contains virtual prioritization component
  scores, but not per-cell-line IC50 values, PIK3CA mutation annotations, or
  GDSC/DepMap sample identifiers.

If raw IC50/PIK3CA table is recovered before resubmission:

- Unit of analysis: cell line.
- Outcome: log10(IC50 in micromolar) for inavolisib.
- Group: PIK3CA-mutant vs PIK3CA-wild-type.
- Test: two-sided Wilcoxon/Mann-Whitney test.
- Effect size: median difference in log10(IC50), with bootstrap 95% CI.
- Report: n per group, median/IQR per group, p value, effect size/CI, and data source/version.
- Interpretation: descriptive sensitivity analysis; not a powered biomarker validation.

If raw IC50/PIK3CA table is not recovered:

- Do not add new statistics.
- Add discussion text that PIK3CA status alone may be insufficient to explain
  modeled inavolisib sensitivity and that drug-prioritization results remain
  computational hypotheses requiring pharmacologic testing.

## 3. Organ-of-origin mregDC signature comparison

Reviewer issue: the 22-sample reference combines cervical, ovarian, and
endometrial cancers; clarify whether basal mregDC signature magnitude varies by
organ of origin.

Available current source data:

- Sample manifest: `source_data/Fig01_study_design_scRNA_reference/Source_Data_Table_S1_scRNA_GEO_sample_manifest.csv`
- Cell feature matrix: `source_data/Fig02_scRNA_mregDC_program/scRNA_cell_marker_feature_matrix.tsv`

Audit finding:

- The sample manifest contains disease group and organ-level sample labels.
- The current cell feature matrix contains cell barcode and mregDC/AP-related
  feature values, but no sample identifier column.

If a cell-to-sample mapping or sample-level mregDC summary is recovered:

- Unit of analysis: sample, not cell.
- Groups: cervical squamous/cervical adenocarcinoma collapsed or reported as
  cervical, ovarian, and endometrial depending on n and reviewer-facing clarity.
- Primary test: Kruskal-Wallis across organs.
- Pairwise tests: Wilcoxon rank-sum with Benjamini-Hochberg adjustment.
- Report: n per organ, median/IQR, p values/q values, and effect sizes.
- Visualization: boxplot with per-sample points.
- Interpretation: descriptive because organ, dataset, platform, and source-study
  effects are partially confounded.

If no cell-to-sample mapping is recovered:

- Do not perform cell-level pseudoreplicated organ testing.
- Add text stating that the 22-sample scRNA cohort provides a pan-gynecologic
  reference and that organ-origin magnitude comparisons are limited by the
  available source-data granularity and dataset/source-study confounding.

## 4. Reviewer-response rule

Before final submission, use past tense only for changes that exist in the
revised manuscript, source-data archive, and public repository. Until then, keep
working drafts marked as pre-edit drafts.
