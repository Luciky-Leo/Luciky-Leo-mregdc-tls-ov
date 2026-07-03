# Supplementary Figure Final Redo Audit

Date: 2026-07-03

## Scope

This audit documents the final supplementary-figure rebuild performed for the Cancers R1 revision package. The rebuild focused on the supplementary figure set, especially spatial transcriptomic panels, while preserving the main figure structure and the revised manuscript claims.

## Output Set

The current supplementary set contains Supplementary Figures S1-S14. Each supplementary figure was standardized to a compact four-panel layout to reduce visual imbalance across the supplement.

Export root:

`E:\Reserch\MregDC_Cancers_R1_Revision_20260629\09_SUP_CNS_redraw_v2_20260703\exports`

Current export formats:

- Editable vector: PDF and SVG
- Raster preview: PNG
- Compiled supplementary PDF: `supplementary_information_rebuild\Supplementary_Information_CNS_v2.pdf`

## Key Redraw Decisions

1. Supplementary Figure S4 was rebuilt to reduce label crowding and align multi-sample spatial validation panels under a uniform visual grammar.
2. Supplementary Figure S10 was rebuilt from isolated dot-like maps into tissue-context spatial field visualization with background cells, TLS-field objects, and co-high bins shown in one coherent spatial frame.
3. Supplementary Figures S8-S14 were retained as structured support figures but converted into the same four-panel supplementary style as S1-S7.
4. Figure legends were kept result-focused; explanatory interpretation remains in the Results or Discussion text.

## Source Data Check

The source-data package now contains explicit source-data folders for all supplementary figures S1-S14:

- `FigS01_singleCellHaystack_audit`
- `FigS02_Hotspot_audit`
- `FigS03_Xenium_spatial_maps`
- `FigS04_multi_sample_spatial_source`
- `FigS05_model_validation`
- `FigS06_specificity_adjustment`
- `FigS07_drug_prioritization_docking`
- `FigS08_scRNA_IF_support`
- `FigS09_Xenium_program_maps`
- `FigS10_Xenium_TLS_fields`
- `FigS11_TLS_distance_gradients`
- `FigS12_immune_deconvolution_context`
- `FigS13_patient_composite_structure`
- `FigS14_virtual_perturbation_support`

The rows for FigS8-FigS14 in `SOURCE_DATA_INDEX.csv` were updated to point to their explicit supplementary source-data folders. These folders contain copied source tables from the authoritative main-figure source-data folders, with no value changes.

Rebuilt source-data archive:

`E:\Reserch\MregDC_Cancers_R1_Revision_20260629\07_submission_package_R1\Source_Data.zip`

Final source-data archive check:

- Total entries: 135
- Explicit S1-S14 folders: present
- Archive size: 45,084,801 bytes

## Manuscript Cross-Reference Check

The revised manuscript text now cites all supplementary figures S1-S14:

- S1-S2: spatial non-randomness audits
- S3, S9, S10: Xenium spatial program and TLS-field support
- S4, S11: multi-sample spatial validation and distance/decile gradients
- S5, S13: model and patient-level composite support
- S6, S12: specificity and immune deconvolution support
- S7, S14: drug and perturbation support
- S8: scRNA and representative IF support

The Data Availability statement was updated from `Supplementary Figs. S1-S7` to `Supplementary Figs. S1-S14`.

## Build And Package Verification

Compiled successfully:

- Main manuscript PDF: `07_submission_package_R1\manuscript_cancers_mdpi_R1.pdf`
- Supplementary information PDF: `09_SUP_CNS_redraw_v2_20260703\supplementary_information_rebuild\Supplementary_Information_CNS_v2.pdf`

Preflight:

- `SUBMISSION_PRECHECK_REPORT.md`: PASS
- Main figures: Fig. 1-Fig. 10 present and cited
- Supplementary figures: S1-S14 present and cited
- Supplementary tables: S1-S3 present and cited

Upload packages rebuilt:

- `07_submission_package_R1\Cancers_R1_LaTeX_Source.zip`
- `07_submission_package_R1\Cancers_R1_Supplementary_Files.zip`
- `07_submission_package_R1\Source_Data.zip`

The LaTeX source archive was rebuilt from a dedicated flat upload staging folder:

`07_submission_package_R1\latex_source_flat_upload_20260703`

The flat LaTeX upload source compiles successfully after moving MDPI template support files to the same folder level and removing `Definitions/` path prefixes from the upload-copy of `mdpi.cls`. The final `Cancers_R1_LaTeX_Source.zip` has:

- First ZIP entry: `manuscript_cancers_mdpi.tex`
- Nested entries: 0
- Maximum file-name length: 30 characters
- Supplementary figure PDFs included: 14

GitHub/Zenodo staging synced:

- `06_github_zenodo_release\Luciky-Leo-mregdc-tls-ov\supplementary`
- `06_github_zenodo_release\Luciky-Leo-mregdc-tls-ov\source_data`
- `06_github_zenodo_release\Luciky-Leo-mregdc-tls-ov\code\supplementary_figure_upgrade_20260703`

## Residual Notes

The supplementary figures are now production-consistent and traceable. The main scientific limitations remain unchanged and should not be overclaimed: representative IF is not a separated-channel tissue-level colocalization assay; spatial antigen-presentation maps use AP/MHC-II proxy scores where direct HLA genes are unavailable; perturbation and drug panels remain computational prioritization rather than functional validation.
