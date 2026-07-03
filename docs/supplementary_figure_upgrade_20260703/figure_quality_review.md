# Figure Quality Review

Scoring follows the local PRISM figure quality protocol. Because these are supplementary figures, `accept_supplement` is the final decision state; scores above 80 indicate the panel set is suitable for the revised supplementary package after legend-level claim boundaries.

| Panel | Option | Candidate ID | Scientific fit | Data fit | Visual clarity | Grammar fidelity | Publication standard | Reproducibility | Reference/layout match | Editable-script readiness | Camera-ready risk | Total score | Decision | Quality problems | Revision action |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| Fig. S1 | final | S1_v2 | 28 | 19 | 18 | 13 | 9 | 5 | 8 | 5 | 4 | 92 | accept_supplement | Dense gene labels limited to top features. | Kept ranked display and moved interpretation to legend. |
| Fig. S2 | final | S2_v2 | 28 | 19 | 18 | 13 | 9 | 5 | 8 | 5 | 4 | 92 | accept_supplement | Hotspot outlier can dominate axis scale. | Kept source-scale axis because it reflects true evidence distribution. |
| Fig. S3 | final | S3_v2 | 30 | 20 | 18 | 14 | 9 | 5 | 9 | 5 | 4 | 96 | accept_supplement | Spatial contour panel is visually dense. | Smoothed contours and retained separate score maps for readability. |
| Fig. S4 | final | S4_v4_uniform_spatial_gallery | 30 | 20 | 19 | 13 | 9 | 5 | 8 | 5 | 4 | 96 | accept_supplement | Spatial maps are overview panels rather than single-sample inspection panels. | Normalized thumbnail coordinates to equal-sized map slots, centered dataset labels, enlarged co-high spots, and tightened panel spacing. |
| Fig. S5 | final | S5_v2 | 29 | 20 | 18 | 13 | 9 | 5 | 8 | 5 | 4 | 94 | accept_supplement | Internal model validation only. | Legend states exploratory/internal validation. |
| Fig. S6 | final | S6_v2 | 30 | 20 | 18 | 13 | 9 | 5 | 8 | 5 | 4 | 95 | accept_supplement | Adjusted Xenium association is weak after controls. | Retained bounded result and moved interpretation to response/manuscript. |
| Fig. S7 | final | S7_v2 | 27 | 18 | 18 | 12 | 9 | 5 | 7 | 5 | 4 | 89 | accept_supplement | Computational screen can be overread as efficacy evidence. | Legend explicitly states hypothesis-generating only. |
| Fig. S8 | final | S8_v3_label_clear | 28 | 18 | 19 | 12 | 9 | 5 | 7 | 5 | 4 | 91 | accept_supplement | IF panel uses representative merged-image raw counts only. | Shortened disease/marker labels and converted grouped IF count bars to a log10(count+1) heatmap to remove legend overlap. |
| Fig. S9 | final | S9_v2 | 30 | 20 | 19 | 14 | 9 | 5 | 9 | 5 | 4 | 97 | accept_supplement | Large coordinate maps can appear sparse in low-score regions. | Kept common coordinate framework and shared visual scale grammar. |
| Fig. S10 | final | S10_v3_tissue_density | 30 | 20 | 18 | 13 | 9 | 5 | 8 | 5 | 4 | 95 | accept_supplement | Field IDs are compact identifiers and should be interpreted through the legend. | Added pale tissue-density background and rescaled field/co-high markers for spatial readability. |
| Fig. S11 | final | S11_v2 | 30 | 20 | 18 | 13 | 9 | 5 | 8 | 5 | 4 | 95 | accept_supplement | Distance-gradient uncertainty widens at far bins. | Kept uncertainty bands and legend-level caution. |
| Fig. S12 | final | S12_v2_refined | 28 | 19 | 18 | 12 | 9 | 5 | 7 | 5 | 4 | 91 | accept_supplement | Ten-method deconvolution is heterogeneous by design. | Aggregated method-level IF associations to avoid row-label clutter. |
| Fig. S13 | final | S13_v2 | 29 | 20 | 18 | 12 | 9 | 5 | 7 | 5 | 4 | 93 | accept_supplement | Patient-level feature atlas is an overview, not an independent validation cohort. | Kept as bridge figure and retained model-validation in S5. |
| Fig. S14 | final | S14_v2 | 28 | 19 | 18 | 12 | 9 | 5 | 7 | 5 | 4 | 91 | accept_supplement | Perturbation is TF/program-level computational inference. | Caption states virtual perturbation hypothesis, not direct wet-lab KO. |

## Residual Risk Notes

- Spatial AP/MHC-II panels use proxy genes where exact HLA class II genes are unavailable in a platform panel.
- Representative IF panels should not be used for Pearson/Manders colocalization claims unless separated raw channels and additional ROIs are provided.
- Drug and perturbation panels are retained as computational prioritization and should not be used to claim therapeutic efficacy.
- Final visual pass on 2026-07-03 removed direct label overlaps in S1/S2/S7, made S4 spatial-map slots equal-sized and title-aligned, shortened crowded labels in S8/S13, and rechecked S1-S14 by contact-sheet and individual-figure preview.
