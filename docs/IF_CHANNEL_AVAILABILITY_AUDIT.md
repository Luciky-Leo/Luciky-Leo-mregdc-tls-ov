# IF raw-channel availability audit for Cancers R1

Date: 2026-06-29

Purpose: respond to the reviewer request for formal IF co-localization statistics
using separated raw channels, while preventing unsupported claims if only merged
images are available.

## Search scope

Checked locations:

- `E:\Reserch\MregDC_Cancers_R1_Revision_20260629`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4_auto_image_quant_20260526`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\figure_logic_reorder_review_20260526\Fig4_recommended_main`
- `F:\Database\04_project_exports_review\mregDC_TLS_OVC_20260611\Cancers_Source_Data_final_20260611`

Targeted file types searched:

- raw or microscopy container formats: `.czi`, `.nd2`, `.lif`, `.lsm`, `.ome.tif`, `.qptiff`, `.svs`
- image stacks: `.tif`, `.tiff`
- channel-indicative file names: `CD11C`, `HLA`, `DRA`, `LAMP3`, `CCR7`, `DAPI`, `channel`, `ch1`, `ch2`, `ch3`, `ch4`, `C01`, `C02`, `C03`, `C04`

## Files found

Current IF-specific available files are merged or derived files:

- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4\OVC.png`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4\CEAD.png`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4\CESC.png`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4\UCEC.png`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4_auto_image_quant_20260526\inputs\OVC.jpg`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4_auto_image_quant_20260526\inputs\CEAD.jpg`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4_auto_image_quant_20260526\inputs\CESC.jpg`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4_auto_image_quant_20260526\inputs\UCEC.jpg`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4_auto_image_quant_20260526\merged_jpg_detected_cells.tsv`
- `F:\Reserch_Archive\mregDC_all_Edrive_20260611\MregDC\fig4_auto_image_quant_20260526\merged_jpg_roi_quantification.tsv`
- `E:\Reserch\MregDC_Cancers_R1_Revision_20260629\03_source_data_working\Fig03_representative_IF_raw_counts\Fig03_IF_ROI_raw_counts.csv`
- `E:\Reserch\MregDC_Cancers_R1_Revision_20260629\03_source_data_working\Fig03_representative_IF_raw_counts\Fig03_IF_raw_count_summary.csv`

The search found exported `.tiff` figure panels elsewhere in the archived project, but these are plot exports or rendered figure assets, not raw separated IF channel stacks.

## Audit conclusion

No raw separated IF channel files were located in the active Cancers R1 workspace,
the archived submitted project tree, or the staged source-data package. Therefore:

- Pearson, Manders, or other channel-wise co-localization statistics should not be performed for the current revision unless the user provides raw separated channel images.
- The current Fig. 3 IF layer should remain framed as representative merged-image tissue visualization.
- Raw ROI counts from flattened merged JPGs may be reported only as illustrative counts, not as per-mm2 density, tissue-level abundance, single-cell four-marker co-positivity, or formal co-localization.
- The reviewer response should transparently state that raw separated channels were unavailable at this revision stage and that the manuscript was revised to avoid unsupported co-localization claims.

## Manuscript wording rule

Use:

- "representative multiplex IF images"
- "merged-image ROI-level illustrative counts"
- "regional CD11C/HLA-DRA/LAMP3/CCR7 co-occurrence"
- "future raw-channel pathology validation"

Avoid:

- "formal IF validation"
- "single-cell four-marker co-localization"
- "Pearson/Manders co-localization"
- "tissue-level density"
- "cross-cancer abundance estimate"

