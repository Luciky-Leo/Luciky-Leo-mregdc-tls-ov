from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path("/mnt/e/Reserch/MregDC")
SRC = ROOT / "ScientificReports_official_template_submission_20260602"
TEMPLATE_ZIP = Path("/mnt/d/XunLei/Download/Springer_Nature_LaTeX_Template.zip")
OUT = ROOT / "JTM_SpringerNature_submission_20260602"


TITLE = (
    "Spatially organized TLS-associated mregDC antigen-presentation fields "
    "define an immune-prognostic context in ovarian cancer"
)
SHORT_TITLE = "TLS-associated mregDC antigen-presentation fields in ovarian cancer"


ABSTRACT = r"""\textbf{Background:} Tertiary lymphoid structures (TLSs) are increasingly recognized as spatially organized immune niches in solid tumors, but how TLS programs relate to mature regulatory dendritic-cell states in ovarian cancer remains incompletely defined.

\textbf{Methods:} We integrated public gynecological tumor scRNA-seq, CD11C/HLA-DRA/LAMP3/CCR7 multiplex immunofluorescence, public Xenium and multi-sample spatial transcriptomics, TCGA-OV immune deconvolution and exploratory prognostic modeling, and in silico regulatory and drug-prioritization analyses. TLS identity was assessed using chemokine/TLS-imprint modules and spatial co-localization, whereas LAMP3/CCR7-enriched dendritic cells were interpreted as a mature migratory mregDC state.

\textbf{Results:} Single-cell analysis resolved a $LAMP3^{+}CCR7^{+}$ dendritic-cell population enriched for mature migratory, antigen-presentation, checkpoint, and NF-$\kappa$B/TNF-associated programs. Representative immunofluorescence detected $CD11C^{+}HLA$-$DRA^{+}LAMP3^{+}CCR7^{+}$ cells within or near immune-enriched tissue regions. Xenium and multi-sample spatial analyses linked TLS-score-defined fields to mregDC, antigen-presentation/MHC-II proxy, and interferon-associated programs, with distance-gradient analyses supporting TLS-proximal enrichment. Ten-method immune deconvolution and immune-richness-adjusted analyses associated the TLS/mregDC field with an immune-infiltrated TCGA-OV contexture, and exploratory patient-level scoring suggested prognostic relevance. scTenifoldKnk and CellOracle prioritized NF-$\kappa$B/antigen-presentation-associated regulatory nodes, and drug-prioritization analyses nominated candidate perturbation classes for experimental testing.

\textbf{Conclusions:} These findings support a translational, hypothesis-generating model in which TLS-associated mregDC antigen-presentation fields represent a spatially organized immune context linked to antigen-presentation programs, patient immune contexture, and candidate regulatory vulnerabilities in ovarian cancer."""


KEYWORDS = (
    "ovarian cancer; tertiary lymphoid structure; mregDC; spatial transcriptomics; "
    "single-cell RNA sequencing; antigen presentation; immune infiltration; translational immuno-oncology"
)


PREAMBLE = rf"""%Version 3.1 December 2024
\documentclass[pdflatex,sn-vancouver-num]{{sn-jnl}}

\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{array}}
\usepackage{{amsmath,amssymb}}
\usepackage{{xcolor}}
\usepackage{{textcomp}}

\raggedbottom

\begin{{document}}

\title[{SHORT_TITLE}]{{{TITLE}}}

\author[1]{{\fnm{{Feifan}} \sur{{Lu}}}}\equalcont{{These authors contributed equally to this work.}}
\author[2]{{\fnm{{Ting}} \sur{{Zhang}}}}\equalcont{{These authors contributed equally to this work.}}
\author[3]{{\fnm{{Zhixuan}} \sur{{Li}}}}
\author[3]{{\fnm{{Renqi}} \sur{{Yao}}}}
\author[4]{{\fnm{{Hao}} \sur{{Hu}}}}
\author*[1]{{\fnm{{Rui}} \sur{{Guan}}}}\email{{cngreen785@163.com}}
\author*[1]{{\fnm{{Mingjuan}} \sur{{Xu}}}}\email{{mingjuanxu@smmu.edu.cn}}

\affil[1]{{\orgdiv{{Department of Obstetrics and Gynecology}}, \orgname{{Changhai Hospital, Naval Medical University}}, \orgaddress{{\city{{Shanghai}}, \postcode{{200433}}, \country{{China}}}}}}
\affil[2]{{\orgdiv{{Department of Hematology}}, \orgname{{Shanghai East Hospital, Tongji University}}, \orgaddress{{\city{{Shanghai}}, \postcode{{200120}}, \state{{Shanghai}}, \country{{China}}}}}}
\affil[3]{{\orgdiv{{National Facility for Translational Medicine (Beijing), Medical Innovation Research Division}}, \orgname{{PLA General Hospital}}, \orgaddress{{\city{{Beijing}}, \postcode{{100853}}, \country{{China}}}}}}
\affil[4]{{\orgdiv{{Department of Pathology}}, \orgname{{Changhai Hospital, Naval Medical University}}, \orgaddress{{\city{{Shanghai}}, \postcode{{200433}}, \country{{China}}}}}}

\abstract{{{ABSTRACT}}}

\keywords{{{KEYWORDS}}}

\maketitle
"""


DECLARATIONS = r"""
\bmhead{Acknowledgements}
The authors thank GEO, TCGA, GTEx, 10x Genomics, and the investigators who generated the public datasets re-analyzed in this study. The authors also thank the patients who contributed clinical specimens to this study. This work was supported by the Foundation of Changhai Hospital (No.~2020YXK024).

\section*{Declarations}

\bmhead{Funding}
This work was supported by the Foundation of Changhai Hospital (No.~2020YXK024).

\bmhead{Competing interests}
The authors declare no competing interests.

\bmhead{Ethics approval and consent to participate}
The use of human clinical specimens in this study was approved by the Ethics Committee of Changhai Hospital, Naval Medical University (approval No.~CHEC 2023-011). Written informed consent was obtained from all participants. Analyses of publicly available GEO, TCGA, GTEx, 10x Genomics, and public spatial transcriptomic datasets used de-identified data and were conducted in accordance with the relevant database policies and journal requirements.

\bmhead{Consent for publication}
Not applicable.

\bmhead{Data availability}
The public scRNA-seq datasets analyzed in this study are available from GEO under accession numbers GSE197461, GSE208653, and GSE173682. GSE197461 and GSE208653 were used for the cervical squamous cell carcinoma and cervical adenocarcinoma components, and GSE173682 was used for the ovarian and endometrial tumor components. The sample-level reconstruction of the 22-sample scRNA-seq cohort is provided in Supplementary Table~S1 and in the Source Data folder. Signature definitions, legacy-label harmonization, and gene-coverage/marker-availability audits are provided in Supplementary Table~S2 and \texttt{source\_data/Tables\_signature\_and\_GEO}. The public 10x Genomics scFFPE ovarian cancer matrix is available from the 10x Genomics 17k human ovarian cancer scFFPE dataset. The public Xenium Prime ovarian cancer FFPE dataset is available from the 10x Genomics Xenium Prime FFPE human ovarian cancer dataset. TCGA-OV RNA-seq and clinical data were retrieved from the Genomic Data Commons, and normal-tissue reference data were retrieved from GTEx. Additional public ovarian spatial transcriptomic datasets used for multi-sample spot-level support are summarized in the Source Data folder. Derived IF ROI-quantification, TLS-score, spatial co-localization, TLS-distance-gradient, ten-method immune-deconvolution, immune-richness-adjusted specificity, patient-level prognostic-model, CellOracle TF-level perturbation, scTenifoldKnk virtual-knockout, virtual-screening, and docking-audit tables generated for Figs.~1--11 and Supplementary Figs.~S1--S6 are included in the Source Data folder accompanying this submission where table output was generated. Additional de-identified data supporting the findings of this study are available from the corresponding authors on reasonable request and subject to institutional and ethical restrictions.

\bmhead{Code availability}
Code used for manuscript assembly, source-data indexing, clinical sensitivity modeling, and reviewer-facing reproducibility checks is available at \url{https://github.com/Luciky-Leo/Luciky-Leo-mregdc-tls-ov} and archived at Zenodo under DOI \url{https://doi.org/10.5281/zenodo.20529436}. Figure-level source-data files are provided in the repository under \texttt{source\_data/} and are mapped to current manuscript figures in \texttt{source\_data/SOURCE\_DATA\_INDEX.csv}. Additional upstream analysis scripts used to derive the single-cell, spatial, immune-deconvolution, perturbation, prognostic-model, and docking source tables are available from the corresponding authors on reasonable request.

\bmhead{Materials availability}
No unique materials were generated in this study.

\bmhead{Author contributions}
Feifan Lu and Ting Zhang contributed equally to this work and share first authorship. Feifan Lu conceived the study, developed the methodology, performed the experiments, and drafted the manuscript. Ting Zhang analyzed the data, validated the results, and critically revised the manuscript. Zhixuan Li and Renqi Yao contributed to experimental design, data interpretation, and technical support. Hao Hu contributed to pathological diagnosis, clinical data analysis, and histopathological review. Rui Guan and Mingjuan Xu supervised the study, acquired funding, and finalized the manuscript. All authors read and approved the final manuscript and agree to be accountable for all aspects of the work.
"""


SUPP_TEX = rf"""\documentclass[pdflatex,sn-vancouver-num]{{sn-jnl}}
\usepackage{{graphicx}}
\usepackage{{amsmath,amssymb}}
\usepackage{{xcolor}}
\raggedbottom

\begin{{document}}

\title[Supplementary information]{{Supplementary information: {TITLE}}}
\author[1]{{\fnm{{Feifan}} \sur{{Lu}}}}
\author[2]{{\fnm{{Ting}} \sur{{Zhang}}}}
\author*[1]{{\fnm{{Rui}} \sur{{Guan}}}}\email{{cngreen785@163.com}}
\author*[1]{{\fnm{{Mingjuan}} \sur{{Xu}}}}\email{{mingjuanxu@smmu.edu.cn}}
\affil[1]{{\orgdiv{{Department of Obstetrics and Gynecology}}, \orgname{{Changhai Hospital, Naval Medical University}}, \orgaddress{{\city{{Shanghai}}, \postcode{{200433}}, \country{{China}}}}}}
\affil[2]{{\orgdiv{{Department of Hematology}}, \orgname{{Shanghai East Hospital, Tongji University}}, \orgaddress{{\city{{Shanghai}}, \postcode{{200120}}, \state{{Shanghai}}, \country{{China}}}}}}
\maketitle

\section*{{Supplementary Figure Legends}}

\begin{{figure}}[ht]
\centering
\includegraphics[width=0.98\textwidth]{{FigureS1_singleCellHaystack.png}}
\caption{{\textbf{{Supplementary Figure S1. singleCellHaystack audit of spatially non-random transcriptional features in the Xenium ovarian cancer section.}} A deterministic 60,000-cell subset was sampled from the public Xenium ovarian cancer FFPE dataset, retaining 1,500 real Xenium genes and matched cell-level spatial coordinates. The ranked-feature panel shows top genes by singleCellHaystack evidence (-log10 adjusted $P$) for non-random spatial organization. The marker-audit panel plots TLS/mregDC/antigen-presentation-associated markers by singleCellHaystack $D_{{KL}}$, with point size reflecting evidence. This analysis supports spatial non-randomness and marker-level audit only; it does not define TLS histological maturity.}}
\label{{figS1}}
\end{{figure}}
\clearpage

\begin{{figure}}[ht]
\centering
\includegraphics[width=0.98\textwidth]{{FigureS2_Hotspot.png}}
\caption{{\textbf{{Supplementary Figure S2. Hotspot spatial-autocorrelation audit of Xenium gene programs.}} A h5ad object was generated from the same deterministic 60,000-cell/1,500-gene Xenium subset, using the count layer and cell-level spatial coordinates as input. The ranked-feature panel shows top genes by Hotspot spatial-autocorrelation Z score. The marker-audit panel summarizes Hotspot Z scores and FDR evidence for TLS/mregDC/antigen-presentation-associated markers, with point size indicating -log10(FDR). Hotspot local-correlation/module construction was skipped because 1,269 FDR-significant genes made pairwise module computation too slow for the current run; therefore, this supplementary figure is interpreted as a formal spatial-autocorrelation analysis, not a Hotspot module analysis.}}
\label{{figS2}}
\end{{figure}}
\clearpage

\begin{{figure}}[ht]
\centering
\includegraphics[width=0.98\textwidth,height=0.72\textheight,keepaspectratio]{{FigureS3_Xenium_spatial_maps-re.pdf}}
\caption{{\textbf{{Supplementary Figure S3. Xenium spatial maps supporting the spatial feature audits.}} The upper module-map row shows the same deterministic Xenium ovarian cancer subset projected on spatial coordinates for TLS integrated score, mregDC/TLS axis, extended mregDC program, antigen-presentation/MHC proxy, and IF-core proxy; pale background cells show the sampled tissue field and warmer colors indicate higher module scores. The singleCellHaystack gene-map block shows representative genes with high non-random spatial-expression evidence, providing a visual check for the ranked-feature audit in Supplementary Fig.~S1. The TLS-score and TLS/mregDC co-high maps show source-data alignment and the location of cells passing the co-high threshold in the same coordinate system. The Hotspot block shows representative genes with strong spatial-autocorrelation evidence, providing a visual check for the Hotspot ranked-feature audit in Supplementary Fig.~S2. These maps are descriptive spatial quality-control and audit visualizations; TLS identity and maturity are not inferred from this figure alone.}}
\label{{figS3}}
\end{{figure}}
\clearpage

\begin{{figure}}[ht]
\centering
\includegraphics[width=0.98\textwidth]{{FigureS4_multi_sample_spatial_validation.png}}
\caption{{\textbf{{Supplementary Figure S4. Expanded multi-sample spatial transcriptomic source-data validation across public ovarian spatial datasets.}} Public ovarian spatial transcriptomic matrices were used for spot-level validation across 23 samples and 56,546 spatial spots/capture locations. mregDC, TLS, and antigen-presentation/MHC-II proxy modules were scored per spot using available genes, including exact HLA-DRA, LAMP3, and CCR7 when present. The displayed panels show spot-level TLS/mregDC co-high observed/expected enrichment, gene-set coverage for scored spatial modules, and exact-marker availability across samples. This supplementary figure provides source-level support for the main Fig.~5 multi-sample spatial analysis but is not a histological TLS-maturation assay.}}
\label{{figS4}}
\end{{figure}}
\clearpage

\begin{{figure}}[ht]
\centering
\includegraphics[width=0.98\textwidth]{{FigureS5_model_validation.png}}
\caption{{\textbf{{Supplementary Figure S5. Supplementary validation of the exploratory TCGA-OV prognostic model.}} Time-dependent ROC curves at 1, 3, and 5 years, LASSO-Cox cross-validation, and calibration-by-risk-quintile plots were generated from the same TCGA-OV patient-level feature matrix used in Figs.~8 and 9. The model included mregDC, antigen-presentation/MHC-II, TLS-12CK, B-cell follicle, Tfh/GC, and NF-$\kappa$B scores after complete-case filtering. These analyses are internal performance checks for exploratory stratification and do not establish a clinically deployable predictor without independent validation.}}
\label{{figS5}}
\end{{figure}}
\clearpage

\begin{{figure}}[ht]
\centering
\includegraphics[width=0.98\textwidth]{{FigureS6_specificity_adjusted_associations.png}}
\caption{{\textbf{{Supplementary Figure S6. Immune-richness-adjusted specificity audit of mregDC/TLS/AP associations.}} Raw and adjusted Spearman correlations are shown for TCGA-OV patient-level scores, multi-sample spatial spots, and Xenium cells. TCGA analyses controlled for broad immune context, tumor purity, B-lineage scores, and T-lineage scores. Multi-sample spatial analyses controlled mregDC--TLS associations for local antigen-presentation/MHC-II, B-cell/TLS, and T-cell-zone scores; reciprocal mregDC--antigen-presentation analyses controlled for TLS, B-cell/TLS, and T-cell-zone scores. Xenium sensitivity analyses controlled for antigen-presentation proxy, interferon-response, tumor-proliferation, and tumor-EMT/invasion programs. The panel is interpreted as a confounding audit rather than causal proof of niche specificity. Exact coefficients and $P$ values are provided in the SourceData\_S6\_specificity folder.}}
\label{{figS6}}
\end{{figure}}
\clearpage

\section*{{Supplementary Source Data}}
\begin{{itemize}}
\item Fig. S1 and Fig. S2: \texttt{{SourceData\_S1\_S2\_spatial\_feature\_audits}}.
\item Fig. S3: \texttt{{SourceData\_S3\_Xenium\_spatial\_maps}}.
\item Fig. S4: \texttt{{SourceData\_S4\_multi\_sample\_spatial}}.
\item Fig. S5: \texttt{{SourceData\_S5\_model\_validation}}.
\item Fig. S6: \texttt{{SourceData\_S6\_specificity}}.
\item Signature definitions and gene-coverage audits are provided in Supplementary Table S2 and SourceData S15.
\end{{itemize}}

\section*{{Supplementary Tables}}
Supplementary Table S1 contains the reconstructed 22-sample scRNA-seq GEO source manifest, disease labels, sample counts, and accession-level summaries.

Supplementary Table S2 contains signature definitions, gene-coverage audits, marker-availability checks, and legacy-label harmonization for the mregDC, TLS, antigen-presentation/MHC-II, IFN, FDC/GC, HEV/stromal, proliferation, and EMT/invasion modules.

\end{{document}}
"""


def convert_body(src_tex: str) -> str:
    start = src_tex.index(r"\section*{Introduction}")
    end = src_tex.index(r"\section*{Acknowledgements}")
    body = src_tex[start:end].strip()
    body = body.replace(r"\section*{", r"\section{")
    body = body.replace(r"\subsection*{", r"\subsection{")
    body = body.replace(r"\begin{figure}[p]", r"\begin{figure}[p]")
    body = body.replace(
        "TIMER and ABIS were run through direct \\textbf{immunedeconv} functions in the local Windows/R environment after the generic wrapper failed for these two methods; TIMER used ovarian cancer as the indication for all TCGA-OV profiles, and ABIS was run on the same TPM patient-level expression matrix.",
        "TIMER and ABIS were run through direct \\textbf{immunedeconv} functions after the generic wrapper failed for these two methods; TIMER used ovarian cancer as the indication for all TCGA-OV profiles, and ABIS was run on the same TPM patient-level expression matrix.",
    )
    body = body.replace(
        "This analysis was designed for translational hypothesis prioritization rather than for immediate clinical drug selection.",
        "This analysis was designed for translational hypothesis prioritization and prioritization of experimentally testable therapeutic axes rather than for immediate clinical drug selection.",
    )
    body = re.sub(r"\\section\{Abbreviations\}", r"\\section*{Abbreviations}", body)
    return body


def copytree_filtered(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "figures").mkdir()
    (OUT / "supplementary").mkdir()
    (OUT / "source_data").mkdir()
    (OUT / "code").mkdir()
    (OUT / "00_template_original").mkdir()

    with zipfile.ZipFile(TEMPLATE_ZIP) as zf:
        zf.extractall(OUT / "00_template_original")
    for name in [
        "sn-jnl.cls",
        "sn-vancouver-num.bst",
        "sn-vancouver-ay.bst",
        "sn-basic.bst",
        "sn-nature.bst",
    ]:
        shutil.copy2(OUT / "00_template_original" / name, OUT / name)

    # Use the finalized figure copies from the current submission package; Fig7 already points to the user-updated version.
    for fig in sorted((SRC / "figures").glob("Fig*.pdf")):
        shutil.copy2(fig, OUT / "figures" / fig.name)

    for item in (SRC / "supplementary").iterdir():
        if item.is_file() and (
            item.name.startswith("FigureS")
            or item.name.startswith("Supplementary_Table")
        ):
            shutil.copy2(item, OUT / "supplementary" / item.name)

    copytree_filtered(SRC / "source_data", OUT / "source_data")

    src_tex = (SRC / "manuscript_scientific_reports_official.tex").read_text(encoding="utf-8")
    body = convert_body(src_tex)
    main_tex = PREAMBLE + "\n\n" + body + "\n\n" + DECLARATIONS + "\n\n\\bibliography{sn-bibliography}\n\n\\end{document}\n"
    (OUT / "manuscript_jtm_springer_nature.tex").write_text(main_tex, encoding="utf-8")
    shutil.copy2(SRC / "sn-bibliography.bib", OUT / "sn-bibliography.bib")
    bib_path = OUT / "sn-bibliography.bib"
    bib = bib_path.read_text(encoding="utf-8")
    bib = bib.replace(
        "  howpublished={Gene Expression Omnibus},\n  year={2023},\n  note={GSE197461; PMID: 37794698}\n}",
        "  editor={{Gene Expression Omnibus}},\n  howpublished={Gene Expression Omnibus},\n  publisher={National Center for Biotechnology Information},\n  year={2023},\n  note={GSE197461; PMID: 37794698}\n}",
    )
    bib_path.write_text(bib, encoding="utf-8")

    (OUT / "supplementary" / "Supplementary_Information_jtm_springer_nature.tex").write_text(SUPP_TEX, encoding="utf-8")
    for name in ["sn-jnl.cls", "sn-vancouver-num.bst", "sn-vancouver-ay.bst", "sn-basic.bst", "sn-nature.bst"]:
        shutil.copy2(OUT / name, OUT / "supplementary" / name)

    shutil.copy2(ROOT / "scripts" / "build_jtm_submission_package.py", OUT / "code" / "build_jtm_submission_package.py")
    (OUT / "code" / "README_CODE_AVAILABILITY.md").write_text(
        "# Code availability for peer review\n\n"
        "This folder contains reviewer-facing scripts used for manuscript assembly, figure compression, dataset-accession table generation, and clinical sensitivity modeling for the Journal of Translational Medicine/Springer Nature submission package. "
        "Figure-level source-data files are provided under ../source_data/ and mapped to current manuscript figure numbers in ../source_data/SOURCE_DATA_INDEX.csv. "
        "Additional upstream analysis scripts used to derive the single-cell, spatial, immune-deconvolution, perturbation, prognostic-model, and docking source tables are available from the corresponding authors on reasonable request.\n",
        encoding="utf-8",
    )
    (OUT / "PROJECT_ENV.md").write_text(
        "# Project environment\n\n"
        "Package generated under the E:/Reserch environment policy.\n\n"
        "- Python utilities: WSL Ubuntu + micromamba env `research-py312`.\n"
        "- LaTeX build: Springer Nature `sn-jnl.cls` template with bundled Tectonic/LaTeX plugin.\n"
        "- Source package: `ScientificReports_official_template_submission_20260602`.\n",
        encoding="utf-8",
    )
    (OUT / "README_JTM_submission.md").write_text(
        f"# Journal of Translational Medicine submission package\n\n"
        f"Target journal: Journal of Translational Medicine.\n\n"
        f"Main manuscript: `manuscript_jtm_springer_nature.tex`.\n\n"
        f"Supplementary information: `supplementary/Supplementary_Information_jtm_springer_nature.tex`.\n\n"
        f"Main figures: `figures/Fig1.pdf` through `figures/Fig11.pdf`.\n\n"
        f"Supplementary figures: `supplementary/FigureS1_*` through `supplementary/FigureS6_*`.\n\n"
        "Editorial changes made for JTM:\n\n"
        "- Migrated from the Scientific Reports class to the Springer Nature `sn-jnl.cls` template.\n"
        "- Reframed the title, abstract, and declarations toward translational immuno-oncology.\n"
        "- Kept the user-confirmed main figure layout with Fig1-Fig11 in the main text.\n"
        "- Retained Supplementary Figs. S1-S6 only.\n"
        "- Removed duplicate acknowledgement headings.\n"
        "- Replaced environment-specific wording such as local Windows/R execution with manuscript-appropriate methods language.\n"
        "- Moved declarations into BMC/Springer Nature-compatible declaration subsections.\n\n"
        "Important remaining submission task: compress large figure PDFs, especially Fig3, before portal upload if the journal system enforces per-file limits.\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()

