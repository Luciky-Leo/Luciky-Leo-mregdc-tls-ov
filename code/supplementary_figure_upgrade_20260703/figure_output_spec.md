# Figure Output Specification

- Target width: 180 mm.
- Max height: 240 mm.
- Actual height: 125-132 mm for the revised supplementary figures.
- Height mode: content-adaptive, fixed per exported figure.
- Font: Arial-compatible sans-serif fallback through Matplotlib; editable vector text retained in SVG/PDF where backend permits.
- Panel label: bold upright A-D.
- Axis title/legend: 7-8 pt target.
- Axis tick/in-figure label: 5.5-7 pt target.
- Line width: 0.5-0.8 pt target.
- PNG dpi: 300.
- Palette: PRISM-compatible immune/spatial palette with magenta for TLS/co-high emphasis, purple for TLS field/mregDC overlays, blue for AP/MHC-II and model/readout layers, red-yellow spatial score ramp, and gray for neutral controls.
- Exports: PDF/SVG plus PNG preview for S1-S14.
- Matplotlib pdf.fonttype: Type 42 configured in the imported base plotting module.
- In-figure status notes: absent from final clean candidates.
- Source rule: no simulated-data substitutes; all panels trace to source tables in `07_submission_package_R1/_source_data_stage`.
- Review exception: IF-derived panels are retained as representative raw-count support and are not used to claim tissue-level cell density or true four-channel single-cell colocalization.
