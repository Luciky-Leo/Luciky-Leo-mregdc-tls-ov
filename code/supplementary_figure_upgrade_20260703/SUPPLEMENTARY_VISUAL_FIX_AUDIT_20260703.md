# Supplementary Visual Fix Audit, 2026-07-03

## User-Flagged Issues

1. Supplementary heatmaps appeared to contain blank cells.
2. Multi-sample spatial maps should be restored to the previous native-coordinate visual style.
3. Editable SVG exports were requested for all supplementary figures.

## Data Audit

The apparent blank cells in Supplementary Figure S10C and S11D were checked against the source matrices.

- Figure S10C: the selected top co-high fields have no variance for `median_mregDC` and `median_T_cell`. These columns become non-informative after z-scoring and are shown as neutral values rather than missing data.
- Figure S11D: the `TLS/mregDC co-high fraction` median is truly zero in TLS deciles 1-9 and rises in decile 10. The pale cells are true zero/near-neutral values, not missing data.

## Visual Fixes

- Added a zero-visible diverging heatmap palette with a light grey center so true zero or no-variance values no longer look like missing white gaps.
- Increased heatmap grid visibility in S10C and S11D using subtle grey cell borders.
- Restored Supplementary Figure S4A to native `x/y` coordinates with equal aspect ratio. The earlier normalized `0-1` coordinate slot layout was removed.
- Updated `figure_layout_spec.tsv` so the S4 layout description matches the restored native-coordinate maps.

## Outputs

- Regenerated Supplementary Figures S1-S14 as PDF, PNG, and SVG.
- Recompiled Supplementary Information PDF from the updated figure PDFs.
- Rebuilt upload packages:
  - `Cancers_R1_Supplementary_Files.zip`
  - `Cancers_R1_LaTeX_Source.zip`
  - `Cancers_R1_Supplementary_Figures_SVG_editable.zip`
- Submission preflight status after sync: PASS.

## Editable SVG Folder

All 14 supplementary figure SVG files are collected in:

`E:\Reserch\MregDC_Cancers_R1_Revision_20260629\09_SUP_CNS_redraw_v2_20260703\supplementary_svg_editable_20260703`
