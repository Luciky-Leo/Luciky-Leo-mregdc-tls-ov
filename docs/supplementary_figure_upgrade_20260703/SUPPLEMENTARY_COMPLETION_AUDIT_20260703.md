# Supplementary Figure Completion Audit

Date: 2026-07-03

## Objective-Derived Requirements

| Requirement | Current evidence | Status |
|---|---|---|
| Integrate unused or de-emphasized main-figure analysis layers into supplementary figures as much as possible. | `SOURCE_DATA_INDEX.csv` maps current Fig. 1-Fig. 10 and Supplementary Figs. S1-S14. The formerly main-text drug-prioritization layer is now Fig. S7. Additional source layers from scRNA/IF, Xenium spatial programs, TLS fields, TLS gradients, immune deconvolution, patient composites, and virtual perturbation are represented in Figs. S8-S14. | Complete for all authoritative source-data folders available in the R1 working package. |
| Keep supplementary figures balanced at approximately 4-6 panels. | `supplementary_figure_contract.md` and `figure_layout_spec.tsv` specify four panels for every Supplementary Figure S1-S14. | Complete. |
| Render from original or explicit source tables using a unified standard. | `panel_source_mapping.md` records each figure's source-data folder, input columns/objects, script, runtime, environment, and output. `figure_output_spec.md` defines 180 mm width, editable vector export, 300 dpi PNG previews, and the shared palette/typography standard. | Complete. |
| Improve spatial figures in particular. | Figs. S3, S4, S9, S10, and S11 use coordinate-level spatial maps, TLS-field segmentation, co-high overlays, distance gradients, and multi-sample spatial support. These panels are rendered from coordinate and score tables, not screenshots. | Complete. |
| Use top-journal-matched figure grammar rather than generic theme skins. | `panel_source_mapping.md` and `source_code_diff_notes.md` record the Science TLS spatial-map, contour, heatmap, gradient, model-validation, and compact supplement grammars used for each figure. | Complete. |
| Perform self-review and iterative optimization. | `figure_quality_review.md` scores all S1-S14 panels on a 100-point scale; `signature_style_review.md` records PRISM style-gate decisions. S10 and S12 were refined after visual review. | Complete. |
| Integrate final figures into a supplementary document with comprehensive legends. | `supplementary_information_rebuild/Supplementary_Information_CNS_v2.tex` includes Supplementary Figs. S1-S14 with A-D panel legends; the compiled PDF is copied to `07_submission_package_R1/Supplementary_Information.pdf`. | Complete. |
| Build upload-ready packages. | `Cancers_R1_Supplementary_Files.zip` contains 18 top-level files: `Supplementary_Information.pdf`, `Supplementary_Figure_S1.pdf` to `Supplementary_Figure_S14.pdf`, and `SuppTableS1.xlsx` to `SuppTableS3.xlsx`. The ZIP has no subfolders and no basename longer than 64 characters. `Cancers_R1_LaTeX_Source.zip` contains the new S1-S14 PDFs and no old `FigureS*_` supplement files. | Complete. |
| Preserve claim boundaries. | Main manuscript supplementary statement lists `Supplementary Figures S1--S14` and states that S7/S14 are exploratory computational layers. `panel_source_mapping.md`, `figure_output_spec.md`, and `signature_style_review.md` retain IF/AP-MHC-II/perturbation boundary notes. | Complete. |

## Source-Data Coverage Audit

| Source layer | Current main figure use | Supplementary figure use | Audit conclusion |
|---|---|---|---|
| `Fig01_study_design_scRNA_reference` | Fig. 1 | Fig. S8 | Cohort/source context retained in main and supplement. |
| `Fig02_scRNA_mregDC_program` | Fig. 2 | Fig. S8 | scRNA mregDC program retained in main and supplement. |
| `Fig03_representative_IF_raw_counts` | Fig. 3 | Fig. S8 | IF raw-count support retained with restricted claim. |
| `Fig04_Xenium_spatial_segmentation` | Fig. 4 | Figs. S3, S9, S10 | Core spatial evidence expanded in supplement. |
| `Fig05_multi_sample_spatial_coupling` | Fig. 5 | Fig. S4 through extended multi-sample spatial source tables | Multi-sample spatial support retained and expanded. |
| `Fig06_TLS_distance_gradient` | Fig. 6 | Fig. S11 | Distance/decile gradients retained and expanded. |
| `Fig07_ten_method_immune_deconvolution` | Fig. 7 | Fig. S12 | Immune-deconvolution context retained and expanded. |
| `Fig08_patient_level_composite` | Fig. 8 | Fig. S13 | Patient-level bridge retained and expanded. |
| `Fig09_LASSO_Cox_internal_validation` | Fig. 9 | Fig. S5 | Model validation moved into supplement. |
| `Fig10_virtual_perturbation` | Fig. 10 | Fig. S14 | Perturbation support retained and boundary-labeled. |
| `Fig11_drug_prioritization_docking` | Removed from main figure set | Fig. S7 | Former main-text drug layer is now a supplementary exploratory figure. |
| `FigS01` to `FigS06` legacy supplement source folders | Not applicable | Figs. S1-S6 | Old supplement analyses were redrawn into balanced four-panel figures. |

## Final Verification

- Export manifest: 14 PDF, 14 PNG, and 14 SVG supplementary figure exports.
- Supplementary document: `Supplementary_Information_CNS_v2.pdf`, 15 pages.
- Final package preflight: PASS.
- Supplementary ZIP: 18 entries; 14 supplementary figure PDFs; zero subfolders; zero long basenames.
- LaTeX source ZIP: 14 new supplementary figure PDFs; zero old `FigureS*_` supplement files; zero long basenames.
- Source Data ZIP: 109 entries with `SOURCE_DATA_INDEX.csv` mapped to FigS1-FigS14.

## Remaining Claim Boundaries

- Representative IF remains raw illustrative ROI-count support and should not be described as separated-channel Pearson/Manders colocalization or tissue-level density validation.
- AP/MHC-II spatial readouts remain proxy scores where exact HLA class II genes are absent from a platform panel.
- Drug-prioritization and virtual perturbation panels remain computational hypotheses and do not establish therapeutic efficacy or wet-lab knockout effects.
