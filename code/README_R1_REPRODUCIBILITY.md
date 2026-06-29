# Cancers R1 reproducibility scripts

This folder contains targeted R1 revision scripts and maps. The purpose is not to
rerun the complete original exploratory pipeline, but to make the submitted main
figure/source-data relationship explicit and reviewer-checkable.

Primary files:

- `figure_panel_script_source_map.csv`: main figure panel to script/source-data map.
- `reproduce_main_figure_panel_sources.py`: validates that every mapped source
  file exists and writes a compact per-panel source summary.

Run from WSL:

```bash
cd /mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629
/mnt/e/WSL/micromamba/bin/micromamba run -n research-py312 python 04_analysis_scripts/reproduce_main_figure_panel_sources.py --project-root .
```

Expected output:

- `04_analysis_scripts/output/panel_source_validation_report.csv`

