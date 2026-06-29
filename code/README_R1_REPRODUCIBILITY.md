# Cancers R1 code and source-data scripts

This folder contains targeted R1 revision scripts and maps. The purpose is not to
rerun the complete exploratory pipeline, but to make the submitted main
figure/source-data relationship explicit and reviewer-checkable.

Primary files:

- `figure_panel_script_source_map_repo.csv`: main figure panel to script/source-data map.
- `validate_main_figure_panel_sources.py`: validates that every mapped source
  file exists and writes a compact per-panel source summary.
- `fig1_scRNA_reference.py`: Fig. 1 scRNA cohort provenance script.
- `fig2_mregDC_program.py`: Fig. 2 mregDC marker/program script.

The Fig. 1 and Fig. 2 scripts generate submitted source-data summaries to
support peer-review checks.

Run from WSL:

```bash
cd /mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629
/mnt/e/WSL/micromamba/bin/micromamba run -n research-py312 python 06_github_zenodo_release/Luciky-Leo-mregdc-tls-ov/code/validate_main_figure_panel_sources.py \
  --project-root 06_github_zenodo_release/Luciky-Leo-mregdc-tls-ov \
  --map code/figure_panel_script_source_map_repo.csv \
  --out code/output/panel_source_validation_report.csv
```

Expected output:

- `code/output/panel_source_validation_report.csv`

Repository-side Fig. 1 and Fig. 2 outputs can be generated with:

```bash
cd /mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629/06_github_zenodo_release/Luciky-Leo-mregdc-tls-ov
/mnt/e/WSL/micromamba/bin/micromamba run -n research-py312 python code/fig1_scRNA_reference.py --project-root .
/mnt/e/WSL/micromamba/bin/micromamba run -n research-py312 python code/fig2_mregDC_program.py --project-root .
```

Expected outputs:

- `code/output/fig1_scRNA_reference/`
- `code/output/fig2_mregdc_program/`
