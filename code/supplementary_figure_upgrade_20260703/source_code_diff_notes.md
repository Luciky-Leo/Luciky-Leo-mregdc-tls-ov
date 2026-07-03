# Source Code Difference Notes

## Reference Style

The supplementary redraw adapts the Science TLS atlas visual grammar and the local PRISM signature style system. The workflow uses project source tables rather than paper screenshots or simulated data.

## Code Files

- `scripts/redraw_supplementary_cns_v2.py`: renders Supplementary Figures S1 through S7.
- `scripts/redraw_extra_unused_panels_s8_s14.py`: renders Supplementary Figures S8 through S14 and the expanded contact sheet.
- `scripts/profile_sup_source_data.py`: profiles source-data folders and records table columns/sizes.

## Main Adaptations

- All supplementary figures were normalized to 4 panels and a 180-mm output width.
- Sentence-like explanatory titles were removed from panels. Only panel labels, compact titles, axes, legends, and colorbars remain.
- S3 spatial colocalization overlay was changed from jagged raw contours to smoothed TLS/mregDC field contours to improve readability without changing source coordinates.
- S4 metric heatmap was reduced to biologically interpretable spatial metrics: TLS/mregDC co-high observed/expected, mregDC-TLS integrated association, mregDC-AP/MHC-II association, and TLS-AP/MHC-II association.
- S10 was refined after visual audit: program labels were shortened, tick sizes reduced, and panel spacing widened.
- S12 panel C was converted from a cluttered feature-by-method list into a method-level IF association summary with median and maximum absolute association values.

## Data/Claim Changes Not Made

- No statistical values were fabricated or replaced.
- No IF density, tissue-level abundance, or four-channel single-cell colocalization claim was added.
- No exact HLA gene signal was asserted when the spatial panel only supports an AP/MHC-II proxy.
- No drug-efficacy or therapeutic-response claim was added from docking/virtual screening.

## Export Size

- PDF/SVG/PNG are exported for S1-S14 under `exports/`.
- Contact-sheet previews are exported under `qc_reports/`.
