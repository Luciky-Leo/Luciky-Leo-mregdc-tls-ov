from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import redraw_supplementary_cns_v2 as viz  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "07_submission_package_R1" / "_source_data_stage"


def read(path: Path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


def save(fig: plt.Figure, name: str) -> None:
    viz.save_all(fig, name)


def numeric(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        try:
            out[col] = pd.to_numeric(out[col])
        except (TypeError, ValueError):
            pass
    return out


def short_decile_readout(label: str) -> str:
    mapping = {
        "MHC-II-high fraction": "AP high",
        "TLS/mregDC co-high fraction": "TLS/mregDC\nco-high",
        "median MHC-II score": "AP score",
        "median mregDC score": "mregDC\nscore",
        "mregDC-high fraction": "mregDC\nhigh",
    }
    return mapping.get(str(label), str(label).replace("_", " "))


def short_immune_corr_label(feature: str, method: str) -> str:
    feature = str(feature)
    method = str(method)
    replacements = {
        "Absolute score (sig score)": "immune score",
        "Absolute score (sig_score)": "immune score",
        "Cytolytic activity": "cytolytic",
        "ImmuneScore": "ImmuneScore",
        "Macrophages M1": "M1 macrophage",
        "Macrophages M2": "M2 macrophage",
        "T cells CD8": "CD8 T",
        "T cells regulatory (Tregs)": "Treg",
        "Plasma cells": "plasma",
    }
    for old, new in replacements.items():
        feature = feature.replace(old, new)
    feature = feature.replace("_", " ").strip()
    return f"{feature[:10]}\n{short_method_abbrev(method)}"


def short_method_label(method: str) -> str:
    mapping = {
        "CIBERSORT_ABS": "CIBERSORT abs",
        "ConsensusTME": "Consensus",
        "MCPcounter": "MCP",
        "quanTIseq": "quanTIseq",
    }
    return mapping.get(str(method), str(method))


def short_method_abbrev(method: str) -> str:
    mapping = {
        "CIBERSORT_ABS": "CIB abs",
        "CIBERSORT": "CIB",
        "ConsensusTME": "Cons",
        "MCPcounter": "MCP",
        "quanTIseq": "qTseq",
        "ESTIMATE": "EST",
    }
    return mapping.get(str(method), str(method)[:7])


def short_feature_label(feature: str) -> str:
    feature = str(feature)
    replacements = {
        "Absolute score (sig score)": "Immune score",
        "Absolute score (sig_score)": "Immune score",
        "Cytotoxic lymphocytes": "Cytotoxic",
        "Macrophages M1": "M1 macrophage",
        "Macrophages M2": "M2 macrophage",
        "Monocytes NC+I": "Monocytes",
        "T cells CD8": "CD8 T",
        "Plasmablasts": "Plasmablast",
    }
    for old, new in replacements.items():
        feature = feature.replace(old, new)
    return feature[:22]


def short_program_label(program: str) -> str:
    mapping = {
        "TLS_integrated": "TLS",
        "TLS_chemokine": "TLS\nchemokine",
        "mregDC": "mregDC",
        "AP_MHCII_proxy": "AP/MHC-II",
        "IFN_response": "IFN",
        "B_cell": "B cell",
        "T_cell": "T cell",
        "FDC_GC_proxy": "FDC/GC",
        "HEV_stromal_proxy": "HEV/stromal",
        "tumor_proliferation": "tumor\nprolif.",
        "tumor_EMT_invasion": "EMT/\ninvasion",
    }
    return mapping.get(str(program), str(program).replace("_", "\n"))


def build_expanded_contact_sheet() -> None:
    files = [
        viz.EXPORT / "FigureS1_singleCellHaystack.png",
        viz.EXPORT / "FigureS2_Hotspot.png",
        viz.EXPORT / "FigureS3_spatial_core.png",
        viz.EXPORT / "FigureS4_multi_sample_spatial_validation.png",
        viz.EXPORT / "FigureS5_model_validation.png",
        viz.EXPORT / "FigureS6_specificity_adjusted_associations.png",
        viz.EXPORT / "Supplementary_Figure_S7_drug_prioritization.png",
        viz.EXPORT / "FigureS8_scRNA_IF_support.png",
        viz.EXPORT / "FigureS9_Xenium_program_maps.png",
        viz.EXPORT / "FigureS10_Xenium_TLS_fields.png",
        viz.EXPORT / "FigureS11_TLS_distance_gradients.png",
        viz.EXPORT / "FigureS12_immune_deconvolution.png",
        viz.EXPORT / "FigureS13_patient_composite.png",
        viz.EXPORT / "FigureS14_perturbation_extras.png",
    ]
    thumbs = []
    for path in files:
        if not path.exists():
            continue
        img = Image.open(path).convert("RGB")
        img.thumbnail((760, 540), Image.Resampling.LANCZOS)
        thumbs.append((path.stem, img.copy()))
    pad = 34
    label_h = 26
    cols = 2
    rows = int(np.ceil(len(thumbs) / cols))
    w = cols * 760 + (cols + 1) * pad
    h = rows * (540 + label_h) + (rows + 1) * pad
    sheet = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
    for i, (name, img) in enumerate(thumbs):
        row = i // cols
        col = i % cols
        x = pad + col * (760 + pad)
        y = pad + row * (540 + label_h + pad)
        draw.text((x, y), name, fill=(17, 24, 39), font=font)
        sheet.paste(img, (x, y + label_h))
    sheet.save(viz.QC / "SUP_CNS_v2_expanded_contact_sheet.png", quality=95)


def draw_s8_scrna_if_support() -> None:
    disease = read(SRC / "Fig01_study_design_scRNA_reference" / "Source_Data_Table_S1_scRNA_GEO_disease_summary.csv")
    svm = read(SRC / "Fig02_scRNA_mregDC_program" / "scRNA_linear_SVM_marker_weights.tsv", sep="\t")
    marker = read(SRC / "Fig02_scRNA_mregDC_program" / "scRNA_cell_marker_feature_matrix.tsv", sep="\t")
    ifraw = read(SRC / "Fig03_representative_IF_raw_counts" / "Fig03_IF_ROI_raw_counts.csv")
    svm["weight"] = pd.to_numeric(svm["weight"], errors="coerce")
    ifraw_cols = ["dapi_nuclei_in_crop", "cd11c_hladra_apc_raw_count", "cd11c_hladra_lamp3_ccr7_regional_cooccurrence_raw_count"]
    for col in ifraw_cols:
        ifraw[col] = pd.to_numeric(ifraw[col], errors="coerce")
    score_cols = [c for c in marker.columns if c != "cell"]
    marker_summary = marker[score_cols].apply(pd.to_numeric, errors="coerce").agg(["mean", "std"]).T.reset_index().rename(columns={"index": "marker"})
    marker_summary = marker_summary.sort_values("mean", ascending=False).head(12)

    fig, axes = plt.subplots(2, 2, figsize=viz.mm_fig(132), gridspec_kw={"wspace": 0.52, "hspace": 0.62})
    axes = axes.ravel()
    viz.panel_label(axes[0], "A")
    disease["disease_short"] = disease["disease_group"].replace(
        {
            "CEAD/ADC": "CEAD",
            "CESC/CSCC": "CESC",
            "UCEC/EC": "UCEC",
        }
    )
    sns.barplot(data=disease, x="disease_short", y="n_samples", ax=axes[0], color=viz.COLORS["tls"], edgecolor="white")
    axes[0].set_title("scRNA-seq sample support", loc="left", fontweight="bold")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("samples")
    sns.despine(ax=axes[0])

    viz.panel_label(axes[1], "B")
    sv = svm.reindex(svm["weight"].abs().sort_values(ascending=False).index).head(12).iloc[::-1]
    sv["marker_label"] = sv["marker"].replace({"MHC_AP_proxy": "MHC/AP"})
    y = np.arange(len(sv))
    axes[1].axvline(0, color="#94A3B8", linewidth=0.7)
    axes[1].hlines(y, 0, sv["weight"], color="#CBD5E1", linewidth=1.0)
    axes[1].scatter(sv["weight"], y, c=np.where(sv["weight"] >= 0, viz.COLORS["risk"], viz.COLORS["green"]), s=22, edgecolor="white", linewidth=0.35)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(sv["marker_label"])
    axes[1].set_xlabel("linear SVM weight")
    axes[1].set_title("marker weights", loc="left", fontweight="bold")
    axes[1].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[1], left=True)

    viz.panel_label(axes[2], "C")
    m = marker_summary.set_index("marker")[["mean", "std"]]
    sns.heatmap((m - m.mean()) / m.std().replace(0, np.nan), ax=axes[2], cmap=viz.DIVERGING_CMAP, center=0, linewidths=0.5, linecolor="white", cbar_kws={"label": "z", "shrink": 0.7})
    axes[2].set_title("marker-score source summary", loc="left", fontweight="bold")
    axes[2].set_xlabel("")
    axes[2].set_ylabel("")
    viz.style_heatmap_ax(axes[2])

    viz.panel_label(axes[3], "D")
    melted = ifraw.melt(id_vars="cancer_type", value_vars=ifraw_cols, var_name="readout", value_name="count")
    label_map = {
        "dapi_nuclei_in_crop": "DAPI\nnuclei",
        "cd11c_hladra_apc_raw_count": "CD11C+\nHLA-DRA+",
        "cd11c_hladra_lamp3_ccr7_regional_cooccurrence_raw_count": "regional\n4-marker",
    }
    melted["readout"] = melted["readout"].map(label_map)
    count_mat = melted.pivot_table(index="cancer_type", columns="readout", values="count", aggfunc="sum")
    count_mat = count_mat.reindex(index=[x for x in ["OVC", "CEAD", "CESC", "UCEC"] if x in count_mat.index])
    count_mat = count_mat[[label_map[c] for c in ifraw_cols if label_map[c] in count_mat.columns]]
    sns.heatmap(
        np.log10(count_mat + 1),
        ax=axes[3],
        cmap=LinearSegmentedColormap.from_list("if_counts", ["#F8FAFC", "#93C5FD", "#DB2777"]),
        linewidths=0.45,
        linecolor="white",
        cbar_kws={"label": "log10(count+1)", "shrink": 0.65},
    )
    axes[3].set_title("representative IF raw counts", loc="left", fontweight="bold")
    axes[3].set_xlabel("")
    axes[3].set_ylabel("")
    viz.style_heatmap_ax(axes[3])
    axes[3].tick_params(axis="x", labelrotation=0, labelsize=5.5)
    axes[3].tick_params(axis="y", labelrotation=0, labelsize=5.8)
    fig.subplots_adjust(left=0.12, right=0.96, top=0.91, bottom=0.13, wspace=0.55, hspace=0.64)
    save(fig, "FigureS8_scRNA_IF_support")


def draw_s9_xenium_program_maps() -> None:
    df = read(SRC / "Fig04_Xenium_spatial_segmentation" / "xenium_tls_program_scores_map_downsample.csv")
    for c in ["x", "y", "TLS_integrated", "mregDC", "AP_MHCII_proxy", "IFN_response"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    fig, axes = plt.subplots(2, 2, figsize=viz.mm_fig(125), gridspec_kw={"wspace": 0.08, "hspace": 0.18})
    panels = [
        ("A", "TLS_integrated", "TLS integrated"),
        ("B", "mregDC", "mregDC"),
        ("C", "AP_MHCII_proxy", "AP/MHC-II proxy"),
        ("D", "IFN_response", "IFN response"),
    ]
    for ax, (lab, col, title) in zip(axes.ravel(), panels):
        viz.panel_label(ax, lab)
        viz.spatial_base(ax, df, title)
        vmin, vmax = viz.quantile_limits(df[col])
        sc = ax.scatter(df["x"], df["y"], c=df[col], s=0.65, cmap=viz.SPATIAL_CMAP, vmin=vmin, vmax=vmax, edgecolor="none", alpha=0.86, rasterized=True)
        cb = fig.colorbar(sc, ax=ax, fraction=0.034, pad=0.01, label="score")
        cb.ax.tick_params(labelsize=5.5)
        cb.set_label("score", fontsize=6)
    save(fig, "FigureS9_Xenium_program_maps")


def draw_s10_xenium_fields() -> None:
    cells = read(SRC / "Fig04_Xenium_spatial_segmentation" / "xenium_tls_program_scores_map_downsample.csv")
    grid = read(SRC / "Fig04_Xenium_spatial_segmentation" / "xenium_tls_field_grid_connected_components.csv")
    obj = read(SRC / "Fig04_Xenium_spatial_segmentation" / "xenium_tls_field_object_metrics.csv")
    avail = read(SRC / "Fig04_Xenium_spatial_segmentation" / "xenium_program_gene_availability.csv")
    for frame in [cells, grid, obj, avail]:
        for col in frame.columns:
            try:
                frame[col] = pd.to_numeric(frame[col])
            except (TypeError, ValueError):
                pass
    fig, axes = plt.subplots(2, 2, figsize=viz.mm_fig(132), gridspec_kw={"wspace": 0.52, "hspace": 0.58})
    axes = axes.ravel()
    viz.panel_label(axes[0], "A")

    x = cells["x"].to_numpy()
    y = cells["y"].to_numpy()
    tissue_counts, xedges, yedges = np.histogram2d(x, y, bins=170)
    tissue_counts = np.ma.masked_where(tissue_counts <= 0, tissue_counts)
    tissue_cmap = LinearSegmentedColormap.from_list(
        "tissue_density", ["#FFFFFF", "#EDF5E9", "#DCE8D4", "#BFD5B7"]
    )
    axes[0].imshow(
        tissue_counts.T,
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        origin="lower",
        cmap=tissue_cmap,
        alpha=0.72,
        interpolation="bilinear",
        aspect="auto",
        zorder=0,
    )
    axes[0].scatter(
        cells["x"],
        cells["y"],
        s=0.18,
        color="#AFC8A6",
        alpha=0.20,
        edgecolor="none",
        rasterized=True,
        zorder=1,
    )
    vmin, vmax = viz.quantile_limits(grid["TLS_grid_mean"])
    sc = axes[0].scatter(
        grid["x"],
        grid["y"],
        s=np.clip(grid["n_cells"] / 3, 5, 24),
        c=grid["TLS_grid_mean"],
        cmap=viz.SPATIAL_CMAP,
        vmin=vmin,
        vmax=vmax,
        edgecolor="white",
        linewidth=0.12,
        alpha=0.94,
        rasterized=True,
        zorder=2,
    )
    high = grid["n_cohigh_cells"] > 0
    axes[0].scatter(
        grid.loc[high, "x"],
        grid.loc[high, "y"],
        s=np.clip(grid.loc[high, "n_cohigh_cells"] * 1.8, 7, 28),
        color=viz.COLORS["cohigh"],
        alpha=0.90,
        edgecolor="white",
        linewidth=0.10,
        rasterized=True,
        zorder=3,
    )
    cb = fig.colorbar(sc, ax=axes[0], fraction=0.035, pad=0.01)
    cb.ax.tick_params(labelsize=5.5)
    cb.set_label("TLS field score", fontsize=6)
    axes[0].set_aspect("equal")
    axes[0].invert_yaxis()
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[0].set_title("TLS-field spatial objects", loc="left", fontweight="bold")
    for spine in axes[0].spines.values():
        spine.set_linewidth(0.45)
        spine.set_color("#94A3B8")

    viz.panel_label(axes[1], "B")
    axes[1].scatter(obj["n_cells"], obj["cohigh_fraction"], s=14, color=viz.COLORS["tls"], alpha=0.6, edgecolor="white", linewidth=0.2)
    axes[1].set_xscale("log")
    axes[1].set_xlabel("field cells")
    axes[1].set_ylabel("co-high fraction")
    axes[1].set_title("field size versus co-highness", loc="left", fontweight="bold")
    axes[1].grid(color="#E5E7EB", linewidth=0.45)
    axes[1].tick_params(labelsize=6)
    sns.despine(ax=axes[1])

    viz.panel_label(axes[2], "C")
    cols = ["median_TLS_integrated", "median_mregDC", "median_AP_MHCII_proxy", "median_IFN_response", "median_B_cell", "median_T_cell", "median_HEV_stromal_proxy", "median_tumor_proliferation"]
    top = (
        obj.assign(cohigh_cells=obj["n_cells"] * obj["cohigh_fraction"])
        .sort_values(["cohigh_fraction", "cohigh_cells"], ascending=False)
        .head(12)
        .set_index("field_id")[cols]
    )
    top.columns = ["TLS", "mregDC", "AP", "IFN", "B", "T", "HEV", "prolif"]
    heat = viz.zscore_frame(top).replace([np.inf, -np.inf], np.nan).fillna(0)
    heat.index = [f"F{int(v)}" for v in heat.index]
    sns.heatmap(
        heat,
        ax=axes[2],
        cmap=viz.ZERO_VISIBLE_CMAP,
        center=0,
        linewidths=0.45,
        linecolor="#CBD5E1",
        cbar_kws={"label": "z", "shrink": 0.58},
    )
    axes[2].set_title("co-high field programs", loc="left", fontweight="bold")
    axes[2].set_xlabel("")
    axes[2].set_ylabel("field")
    viz.style_heatmap_ax(axes[2])
    axes[2].tick_params(axis="x", labelsize=5.8, rotation=35)
    axes[2].tick_params(axis="y", labelsize=5.5)

    viz.panel_label(axes[3], "D")
    avail["coverage"] = avail["n_present"] / avail["n_requested"].replace(0, np.nan)
    y = np.arange(len(avail))
    axes[3].barh(y, avail["coverage"], color=viz.COLORS["ap"], alpha=0.75)
    axes[3].set_yticks(y)
    axes[3].set_yticklabels([short_program_label(v) for v in avail["program"]])
    axes[3].set_xlim(0, 1.05)
    axes[3].set_xlabel("gene coverage")
    axes[3].set_title("panel gene coverage", loc="left", fontweight="bold")
    axes[3].tick_params(axis="y", labelsize=5.5)
    axes[3].tick_params(axis="x", labelsize=6)
    sns.despine(ax=axes[3], left=True)
    save(fig, "FigureS10_Xenium_TLS_fields")


def draw_s11_tls_distance_gradients() -> None:
    dist = read(SRC / "Fig06_TLS_distance_gradient" / "xenium_distance_to_tls_field_program_gradients.csv")
    dec = read(SRC / "Fig06_TLS_distance_gradient" / "multi_sample_spatial_extended_tls_decile_summary.csv")
    long = read(SRC / "Fig06_TLS_distance_gradient" / "multi_sample_spatial_extended_tls_decile_long.csv")
    for frame in [dist, dec, long]:
        for col in frame.columns:
            try:
                frame[col] = pd.to_numeric(frame[col])
            except (TypeError, ValueError):
                pass
    fig, axes = plt.subplots(2, 2, figsize=viz.mm_fig(125), gridspec_kw={"wspace": 0.45, "hspace": 0.55})
    axes = axes.ravel()
    viz.panel_label(axes[0], "A")
    programs = ["TLS_integrated", "mregDC", "AP_MHCII_proxy", "IFN_response"]
    palette = dict(zip(programs, [viz.COLORS["tls"], viz.COLORS["mregdc"], viz.COLORS["ap"], viz.COLORS["cohigh"]]))
    for prog in programs:
        g = dist[dist["program"] == prog]
        axes[0].plot(g["distance_mid_um"], g["mean_score"], color=palette[prog], linewidth=1.3, label=prog.replace("_", " "))
        axes[0].fill_between(g["distance_mid_um"], g["lower95"], g["upper95"], color=palette[prog], alpha=0.12)
    axes[0].set_xlabel("distance to TLS field (um)")
    axes[0].set_ylabel("mean score")
    axes[0].set_title("Xenium distance gradients", loc="left", fontweight="bold")
    axes[0].legend(frameon=False, fontsize=5)
    axes[0].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[0])

    viz.panel_label(axes[1], "B")
    for metric, color in [("median_mregDC", viz.COLORS["mregdc"]), ("median_antigen_presentation_MHCII", viz.COLORS["ap"]), ("median_TLS_integrated", viz.COLORS["tls"])]:
        g = dec.groupby("TLS_decile")[metric].median().reset_index()
        axes[1].plot(g["TLS_decile"], g[metric], marker="o", markersize=3, linewidth=1.3, color=color, label=metric.replace("median_", "").replace("_", " "))
    axes[1].set_xlabel("TLS score decile")
    axes[1].set_ylabel("median z score")
    axes[1].set_title("multi-sample TLS-decile programs", loc="left", fontweight="bold")
    axes[1].legend(frameon=False, fontsize=5)
    axes[1].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[1])

    viz.panel_label(axes[2], "C")
    for metric, color in [("mregDC_high_fraction", viz.COLORS["mregdc"]), ("antigen_presentation_MHCII_high_fraction", viz.COLORS["ap"]), ("TLS_mregDC_cohigh_fraction", viz.COLORS["cohigh"])]:
        g = dec.groupby("TLS_decile")[metric].median().reset_index()
        axes[2].plot(g["TLS_decile"], g[metric], marker="o", markersize=3, linewidth=1.3, color=color, label=metric.replace("_fraction", "").replace("_", " "))
    axes[2].set_xlabel("TLS score decile")
    axes[2].set_ylabel("fraction")
    axes[2].set_title("co-high fraction by TLS decile", loc="left", fontweight="bold")
    axes[2].legend(frameon=False, fontsize=5)
    axes[2].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[2])

    viz.panel_label(axes[3], "D")
    piv = long.pivot_table(index="readout", columns="TLS_decile", values="value", aggfunc="median")
    piv.index = [short_decile_readout(x) for x in piv.index]
    sns.heatmap(
        piv,
        ax=axes[3],
        cmap=viz.ZERO_VISIBLE_CMAP,
        center=0,
        linewidths=0.45,
        linecolor="#CBD5E1",
        cbar_kws={"label": "median", "shrink": 0.65},
    )
    axes[3].set_title("decile readout matrix", loc="left", fontweight="bold")
    axes[3].set_xlabel("TLS decile")
    axes[3].set_ylabel("")
    viz.style_heatmap_ax(axes[3])
    save(fig, "FigureS11_TLS_distance_gradients")


def draw_s12_immune_deconv() -> None:
    status = read(SRC / "Fig07_ten_method_immune_deconvolution" / "Fig07_immune_10method_status_TIMER_ABIS.tsv", sep="\t")
    atlas = read(SRC / "Fig07_ten_method_immune_deconvolution" / "Fig07_CH_immune_method_atlas_TIMER_ABIS_source_matrix.csv")
    corr = read(SRC / "Fig07_ten_method_immune_deconvolution" / "Fig07_immune_correlations_with_TIMER_ABIS.tsv", sep="\t")
    for col in ["rho", "p_adj", "abs_ifcore"]:
        if col in corr.columns:
            corr[col] = pd.to_numeric(corr[col], errors="coerce")
    fig, axes = plt.subplots(2, 2, figsize=viz.mm_fig(125), gridspec_kw={"wspace": 0.55, "hspace": 0.55})
    axes = axes.ravel()
    viz.panel_label(axes[0], "A")
    status["ok_int"] = status["ok"].astype(str).str.lower().eq("true").astype(int)
    status["method_short"] = status["method_label"].map(short_method_label)
    sns.barplot(data=status, y="method_label", x="n_features", hue="ok_int", ax=axes[0], dodge=False, palette={1: viz.COLORS["green"], 0: viz.COLORS["risk"]})
    axes[0].set_yticks(range(status.shape[0]))
    axes[0].set_yticklabels(status["method_short"])
    axes[0].set_title("ten-method run status", loc="left", fontweight="bold")
    axes[0].set_xlabel("features")
    axes[0].set_ylabel("")
    axes[0].legend([], [], frameon=False)
    sns.despine(ax=axes[0], left=True)

    viz.panel_label(axes[1], "B")
    mat = atlas.set_index("row_label").drop(columns=["immune_class"])
    mat = mat.apply(pd.to_numeric, errors="coerce").dropna(how="all").head(18)
    mat.index = [short_feature_label(x.split("|")[0].replace("_", " ")) for x in mat.index]
    sns.heatmap(mat, ax=axes[1], cmap=viz.PRIORITY_CMAP, linewidths=0.25, linecolor="white", cbar_kws={"label": "rho", "shrink": 0.65})
    axes[1].set_title("immune-method atlas", loc="left", fontweight="bold")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("")
    viz.style_heatmap_ax(axes[1])

    viz.panel_label(axes[2], "C")
    method_summary = (
        corr.dropna(subset=["rho"])
        .assign(abs_rho=lambda d: d["rho"].abs(), method_short=lambda d: d["method_label"].map(short_method_label))
        .groupby("method_short")
        .agg(median_abs_rho=("abs_rho", "median"), max_abs_rho=("abs_rho", "max"), n_features=("clean_feature", "nunique"))
        .sort_values("median_abs_rho", ascending=True)
    )
    y = np.arange(len(method_summary))
    axes[2].barh(y, method_summary["median_abs_rho"], color="#E2E8F0", edgecolor="white", height=0.68)
    axes[2].scatter(method_summary["max_abs_rho"], y, color=viz.COLORS["cohigh"], s=22, edgecolor="white", linewidth=0.35, zorder=3, label="max")
    axes[2].set_yticks(y)
    axes[2].set_yticklabels(method_summary.index)
    axes[2].tick_params(axis="y", labelsize=5.2)
    axes[2].set_xlabel("absolute rho with IF core")
    axes[2].set_title("method-level IF associations", loc="left", fontweight="bold")
    axes[2].legend(frameon=False, loc="lower right")
    axes[2].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[2], left=True)

    viz.panel_label(axes[3], "D")
    cls = corr.dropna(subset=["rho"]).groupby("immune_class")["rho"].median().sort_values()
    y = np.arange(len(cls))
    axes[3].barh(y, cls.values, color=[viz.COLORS["ap"] if v < 0 else viz.COLORS["cohigh"] for v in cls.values], alpha=0.85)
    axes[3].axvline(0, color="#94A3B8", linewidth=0.7)
    axes[3].set_yticks(y)
    axes[3].set_yticklabels(cls.index)
    axes[3].set_xlabel("median rho")
    axes[3].set_title("immune-class summary", loc="left", fontweight="bold")
    sns.despine(ax=axes[3], left=True)
    fig.subplots_adjust(left=0.19, right=0.96, top=0.92, bottom=0.12, wspace=0.66, hspace=0.58)
    save(fig, "FigureS12_immune_deconvolution")


def draw_s13_patient_composite() -> None:
    feat = read(SRC / "Fig08_patient_level_composite" / "tcga_tls_patient_features.tsv", sep="\t")
    risk = read(SRC / "Fig08_patient_level_composite" / "tcga_tls_risk_scores.tsv", sep="\t")
    for df in [feat, risk]:
        for col in df.columns:
            if col not in ["patient_id", "risk_group"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    cols = ["TLS_integrated_score", "MregDC_TLS_axis_score", "mregDC_extended_score", "AP_MHCII_score", "IF_core_4marker_score", "Checkpoint_score", "NFkB_score"]
    fig, axes = plt.subplots(2, 2, figsize=viz.mm_fig(125), gridspec_kw={"wspace": 0.45, "hspace": 0.55})
    axes = axes.ravel()
    viz.panel_label(axes[0], "A")
    sample = feat.sort_values("TLS_integrated_score").iloc[:: max(1, len(feat) // 80), :].set_index("patient_id")[cols]
    sample.columns = ["TLS", "axis", "mregDC", "AP", "IF", "Chkpt", "NFkB"]
    sns.heatmap(viz.zscore_frame(sample), ax=axes[0], cmap=viz.DIVERGING_CMAP, center=0, xticklabels=True, yticklabels=False, cbar_kws={"label": "z", "shrink": 0.65})
    axes[0].set_title("patient-feature atlas subset", loc="left", fontweight="bold")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("patients ordered by TLS")

    viz.panel_label(axes[1], "B")
    merged = risk.merge(feat[["patient_id", "TLS_integrated_score", "MregDC_TLS_axis_score", "AP_MHCII_score"]], on="patient_id", suffixes=("_risk", ""))
    long = merged.melt(id_vars="risk_group", value_vars=["TLS_integrated_score", "MregDC_TLS_axis_score", "AP_MHCII_score"], var_name="score", value_name="value")
    sns.boxplot(data=long, x="score", y="value", hue="risk_group", ax=axes[1], palette={"Low": viz.COLORS["green"], "High": viz.COLORS["risk"]}, fliersize=0, width=0.55)
    axes[1].set_xticks(range(3))
    axes[1].set_xticklabels(["TLS", "axis", "AP"], rotation=25, ha="right")
    axes[1].set_title("risk-group score shifts", loc="left", fontweight="bold")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("z score")
    axes[1].legend(frameon=False, fontsize=5)
    sns.despine(ax=axes[1])

    viz.panel_label(axes[2], "C")
    axes[2].hist(risk["risk_score"], bins=26, color="#CBD5E1", edgecolor="white")
    for group, color in [("Low", viz.COLORS["green"]), ("High", viz.COLORS["risk"])]:
        axes[2].axvline(risk.loc[risk["risk_group"] == group, "risk_score"].median(), color=color, linewidth=1.2, label=group)
    axes[2].set_xlabel("risk score")
    axes[2].set_ylabel("patients")
    axes[2].set_title("risk-score distribution", loc="left", fontweight="bold")
    axes[2].legend(frameon=False)
    sns.despine(ax=axes[2])

    viz.panel_label(axes[3], "D")
    corr = feat[cols].corr(method="spearman")
    corr.index = corr.columns = ["TLS", "axis", "mregDC", "AP", "IF", "Chkpt", "NFkB"]
    sns.heatmap(corr, ax=axes[3], cmap=viz.DIVERGING_CMAP, center=0, vmin=-1, vmax=1, linewidths=0.45, linecolor="white", cbar_kws={"label": "rho", "shrink": 0.65})
    axes[3].set_title("patient-level correlation", loc="left", fontweight="bold")
    viz.style_heatmap_ax(axes[3])
    save(fig, "FigureS13_patient_composite")


def draw_s14_perturbation_extras() -> None:
    mat = read(SRC / "Fig10_virtual_perturbation" / "Fig10_CH_virtual_perturbation_matrix_source_matrix.csv")
    tf = read(SRC / "Fig10_virtual_perturbation" / "Source_Data_CellOracle_TF_perturbation_summary.tsv", sep="\t")
    shifts = read(SRC / "Fig10_virtual_perturbation" / "Source_Data_CellOracle_target_gene_shifts.tsv", sep="\t")
    for df in [mat, tf, shifts]:
        for col in df.columns:
            if col not in ["feature", "perturbed_TF", "target_gene"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    fig, axes = plt.subplots(2, 2, figsize=viz.mm_fig(125), gridspec_kw={"wspace": 0.45, "hspace": 0.55})
    axes = axes.ravel()
    viz.panel_label(axes[0], "A")
    m = mat.set_index("feature")
    sns.heatmap(m, ax=axes[0], cmap=viz.DIVERGING_CMAP, center=0, linewidths=0.45, linecolor="white", cbar_kws={"label": "delta", "shrink": 0.65})
    axes[0].set_title("virtual perturbation matrix", loc="left", fontweight="bold")
    viz.style_heatmap_ax(axes[0])

    viz.panel_label(axes[1], "B")
    y = np.arange(len(tf))
    axes[1].scatter(tf["IF_core_mean_delta"], y, color=viz.COLORS["tls"], s=20, label="IF core")
    axes[1].scatter(tf["antigen_presentation_proxy_delta"], y, color=viz.COLORS["ap"], s=20, label="AP proxy")
    axes[1].axvline(0, color="#94A3B8", linewidth=0.7)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(tf["perturbed_TF"])
    axes[1].set_xlabel("mean delta")
    axes[1].set_title("CellOracle TF deltas", loc="left", fontweight="bold")
    axes[1].legend(frameon=False, fontsize=5)
    axes[1].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[1], left=True)

    viz.panel_label(axes[2], "C")
    piv = shifts.pivot_table(index="perturbed_TF", columns="target_gene", values="mean_delta", aggfunc="mean")
    keep_cols = piv.abs().mean().sort_values(ascending=False).head(10).index
    keep_rows = piv.abs().mean(axis=1).sort_values(ascending=False).head(10).index
    sns.heatmap(piv.loc[keep_rows, keep_cols], ax=axes[2], cmap=viz.DIVERGING_CMAP, center=0, linewidths=0.45, linecolor="white", cbar_kws={"label": "delta", "shrink": 0.65})
    axes[2].set_title("target-gene shifts", loc="left", fontweight="bold")
    viz.style_heatmap_ax(axes[2])

    viz.panel_label(axes[3], "D")
    burden = shifts.assign(abs_delta=shifts["mean_delta"].abs()).groupby("perturbed_TF")["abs_delta"].mean().sort_values()
    axes[3].barh(np.arange(len(burden)), burden.values, color=viz.COLORS["cohigh"], alpha=0.8)
    axes[3].set_yticks(np.arange(len(burden)))
    axes[3].set_yticklabels(burden.index)
    axes[3].set_xlabel("mean absolute target shift")
    axes[3].set_title("target-shift burden", loc="left", fontweight="bold")
    sns.despine(ax=axes[3], left=True)
    save(fig, "FigureS14_perturbation_extras")


def main() -> None:
    viz.setup_style()
    draw_s8_scrna_if_support()
    draw_s9_xenium_program_maps()
    draw_s10_xenium_fields()
    draw_s11_tls_distance_gradients()
    draw_s12_immune_deconv()
    draw_s13_patient_composite()
    draw_s14_perturbation_extras()
    build_expanded_contact_sheet()
    viz.write_render_manifest()


if __name__ == "__main__":
    main()
