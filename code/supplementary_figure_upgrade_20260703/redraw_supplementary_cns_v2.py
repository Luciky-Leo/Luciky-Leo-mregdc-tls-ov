from __future__ import annotations

import math
import textwrap
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.lines import Line2D
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
REDRAW = Path(__file__).resolve().parents[1]
SRC = ROOT / "07_submission_package_R1" / "_source_data_stage"
OUT = REDRAW / "outputs"
EXPORT = REDRAW / "exports"
QC = REDRAW / "qc_reports"
for directory in [OUT, EXPORT, QC]:
    directory.mkdir(parents=True, exist_ok=True)


MM = 1 / 25.4
FIG_W = 180 * MM
FIG_H = 125 * MM
FIG_H_TALL = 140 * MM


COLORS = {
    "tls": "#7C3AED",
    "mregdc": "#D97706",
    "ap": "#2563EB",
    "cohigh": "#DB2777",
    "green": "#059669",
    "grey": "#64748B",
    "tissue": "#DCE8D4",
    "risk": "#B91C1C",
}

DATASET_COLORS = {
    "10x Visium": "#C9A400",
    "GSE211956": "#2563EB",
    "GSE224335": "#0891B2",
    "GSE274657": "#DB2777",
    "GSE288483": "#059669",
}

SPATIAL_CMAP = LinearSegmentedColormap.from_list(
    "tls_spatial", ["#EEF4E8", "#F7E3A1", "#FCA85F", "#D63F5D"]
)
PRIORITY_CMAP = LinearSegmentedColormap.from_list(
    "priority", ["#F8FAFC", "#F7C8D8", "#DB2777"]
)
DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "diverging_prism", ["#1D4ED8", "#F8FAFC", "#B91C1C"]
)
ZERO_VISIBLE_CMAP = LinearSegmentedColormap.from_list(
    "zero_visible_diverging", ["#1D4ED8", "#E5E7EB", "#B91C1C"]
)


def setup_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "Arial",
            "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "axes.linewidth": 0.65,
            "axes.edgecolor": "#1F2937",
            "axes.labelcolor": "#111827",
            "xtick.color": "#111827",
            "ytick.color": "#111827",
            "xtick.major.width": 0.55,
            "ytick.major.width": 0.55,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "axes.titlesize": 8,
            "axes.labelsize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "legend.fontsize": 6,
            "figure.dpi": 150,
            "savefig.dpi": 450,
        }
    )
    sns.set_context("paper")
    sns.set_style("white")


def read_csv(path: Path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


def mm_fig(height_mm: float = 125) -> tuple[float, float]:
    return FIG_W, height_mm * MM


def clean_label(text: str, width: int = 24) -> str:
    text = str(text)
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.105,
        1.095,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        fontweight="bold",
        color="#111827",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=0.35),
        clip_on=False,
        zorder=20,
    )


def short_metric_name(name: str) -> str:
    mapping = {
        "mregDC~TLS integrated": "mDC\nTLS",
        "mregDC~TLS 12CK": "mDC\n12CK",
        "mregDC~TLS imprint": "mDC\nimprint",
        "mregDC~antigen-presentation/MHC-II": "mDC\nAP",
        "TLS~antigen-presentation/MHC-II": "TLS-AP",
        "TLS/mregDC co-high O/E": "O/E",
    }
    return mapping.get(str(name), str(name))


def short_signature(name: str) -> str:
    mapping = {
        "AP_MHCII": "AP\nMHCII",
        "B_cell_TLS": "B cell",
        "T_cell_zone": "T zone",
        "TLS_12CK": "TLS 12",
        "TLS_29_imprint": "TLS 29",
        "mregDC": "mregDC",
    }
    return mapping.get(str(name), str(name))


def short_layer_name(name: str) -> str:
    mapping = {
        "TCGA patient": "TCGA",
        "multi-sample spatial spot": "spatial\nspot",
        "spatial spot by dataset": "spatial\ndataset",
        "Xenium cell": "Xenium",
    }
    return mapping.get(str(name), str(name))


def quantile_limits(values: pd.Series, low: float = 0.01, high: float = 0.99) -> tuple[float, float]:
    arr = pd.to_numeric(values, errors="coerce").dropna().to_numpy()
    if arr.size == 0:
        return 0.0, 1.0
    lo, hi = np.quantile(arr, [low, high])
    if not np.isfinite(lo) or not np.isfinite(hi) or lo == hi:
        lo, hi = float(np.nanmin(arr)), float(np.nanmax(arr))
    if lo == hi:
        hi = lo + 1.0
    return float(lo), float(hi)


def zscore_frame(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.apply(pd.to_numeric, errors="coerce")
    return (numeric - numeric.mean(axis=0)) / numeric.std(axis=0).replace(0, np.nan)


def lollipop(
    ax: plt.Axes,
    data: pd.DataFrame,
    y_col: str,
    x_col: str,
    color: str,
    xlabel: str,
    n: int = 14,
) -> None:
    plot = data.sort_values(x_col, ascending=False).head(n).iloc[::-1]
    y = np.arange(plot.shape[0])
    ax.hlines(y, 0, plot[x_col], color="#CBD5E1", linewidth=1.0, zorder=1)
    ax.scatter(plot[x_col], y, s=18, color=color, edgecolor="white", linewidth=0.35, zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels(plot[y_col])
    ax.tick_params(axis="y", labelsize=5.5, pad=1.0)
    ax.set_ylim(-0.6, len(y) - 0.4)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=ax, left=True, bottom=False)


def annotate_ranked_points(
    ax: plt.Axes,
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    label_col: str,
    color: str,
    n: int = 6,
) -> None:
    """Direct-label selected points while enforcing minimum vertical spacing."""
    plot = data.dropna(subset=[x_col, y_col]).sort_values(y_col, ascending=False).head(n).copy()
    if plot.empty:
        return
    ax.margins(x=0.08, y=0.10)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x_span = xlim[1] - xlim[0]
    y_span = ylim[1] - ylim[0]
    min_sep = 0.065 * y_span
    y_text = plot[y_col].to_numpy(dtype=float)
    order = np.argsort(y_text)
    y_sorted = y_text[order].copy()
    low = ylim[0] + 0.04 * y_span
    high = ylim[1] - 0.04 * y_span
    y_sorted = np.clip(y_sorted, low, high)
    for i in range(1, len(y_sorted)):
        if y_sorted[i] - y_sorted[i - 1] < min_sep:
            y_sorted[i] = y_sorted[i - 1] + min_sep
    if len(y_sorted) and y_sorted[-1] > high:
        y_sorted -= y_sorted[-1] - high
    y_final = np.empty_like(y_sorted)
    y_final[order] = y_sorted
    for (_, row), y_lab in zip(plot.iterrows(), y_final):
        x = float(row[x_col])
        y = float(row[y_col])
        place_right = x < (xlim[0] + 0.78 * x_span)
        x_lab = x + (0.025 * x_span if place_right else -0.025 * x_span)
        ha = "left" if place_right else "right"
        ax.annotate(
            str(row[label_col]),
            xy=(x, y),
            xytext=(x_lab, float(y_lab)),
            textcoords="data",
            ha=ha,
            va="center",
            fontsize=5.7,
            color=color,
            bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.88),
            arrowprops=dict(arrowstyle="-", color="#94A3B8", lw=0.35, shrinkA=0, shrinkB=2),
            zorder=8,
            clip_on=False,
        )


def style_heatmap_ax(ax: plt.Axes) -> None:
    ax.tick_params(axis="x", labelrotation=35, length=0)
    ax.tick_params(axis="y", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)


def save_all(fig: plt.Figure, basename: str) -> None:
    fig.savefig(EXPORT / f"{basename}.pdf", facecolor="white")
    fig.savefig(EXPORT / f"{basename}.svg", facecolor="white")
    fig.savefig(EXPORT / f"{basename}.png", facecolor="white", dpi=450)
    fig.savefig(OUT / f"{basename}.png", facecolor="white", dpi=300)
    plt.close(fig)


def read_haystack() -> pd.DataFrame:
    hay = read_csv(
        SRC / "FigS01_singleCellHaystack_audit" / "SourceData_FigS1_singleCellHaystack_ranked_features.tsv",
        sep="\t",
    )
    for col in ["D_KL", "log.p.vals", "log.p.adj"]:
        hay[col] = pd.to_numeric(hay[col], errors="coerce")
    if hay["log.p.adj"].median(skipna=True) < 0:
        hay["evidence"] = -hay["log.p.adj"]
    else:
        hay["evidence"] = hay["log.p.adj"]
    hay["rank"] = np.arange(1, hay.shape[0] + 1)
    return hay.rename(columns={"gene": "Gene"})


def read_hotspot() -> pd.DataFrame:
    hs = read_csv(
        SRC / "FigS02_Hotspot_audit" / "SourceData_FigS2_Hotspot_autocorrelations.tsv",
        sep="\t",
    )
    for col in ["C", "Z", "Pval", "FDR"]:
        hs[col] = pd.to_numeric(hs[col], errors="coerce")
    hs["minus_log10_FDR"] = -np.log10(hs["FDR"].clip(lower=1e-300))
    hs["rank"] = np.arange(1, hs.shape[0] + 1)
    return hs


def draw_s1() -> None:
    hay = read_haystack()
    fig, axes = plt.subplots(2, 2, figsize=mm_fig(125), gridspec_kw={"wspace": 0.45, "hspace": 0.55})
    axes = axes.ravel()

    panel_label(axes[0], "A")
    lollipop(axes[0], hay, "Gene", "evidence", COLORS["mregdc"], "-log10(adjusted P)")
    axes[0].set_title("singleCellHaystack top spatial genes", loc="left", fontweight="bold")

    panel_label(axes[1], "B")
    axes[1].scatter(
        hay["D_KL"],
        hay["evidence"],
        s=8,
        color="#94A3B8",
        alpha=0.55,
        edgecolor="none",
    )
    top = hay.sort_values("evidence", ascending=False).head(8)
    axes[1].scatter(top["D_KL"], top["evidence"], s=20, color=COLORS["cohigh"], edgecolor="white", linewidth=0.35)
    annotate_ranked_points(axes[1], top, "D_KL", "evidence", "Gene", COLORS["cohigh"], n=6)
    axes[1].set_xlabel("D_KL")
    axes[1].set_ylabel("-log10(adjusted P)")
    axes[1].set_title("effect-size and evidence concordance", loc="left", fontweight="bold")
    axes[1].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[1])

    panel_label(axes[2], "C")
    top12 = hay.sort_values("evidence", ascending=False).head(12).set_index("Gene")
    mat = top12[["D_KL", "evidence"]].copy()
    mat["rank evidence"] = -top12["rank"]
    mat_z = zscore_frame(mat)
    sns.heatmap(
        mat_z,
        ax=axes[2],
        cmap=DIVERGING_CMAP,
        center=0,
        cbar_kws={"label": "z", "shrink": 0.7},
        linewidths=0.55,
        linecolor="white",
    )
    axes[2].set_title("top-gene metric matrix", loc="left", fontweight="bold")
    axes[2].set_xlabel("")
    axes[2].set_ylabel("")
    style_heatmap_ax(axes[2])

    panel_label(axes[3], "D")
    plot = hay.sort_values("rank")
    axes[3].plot(plot["rank"], plot["evidence"], color=COLORS["mregdc"], linewidth=1.4)
    axes[3].fill_between(plot["rank"], plot["evidence"], color=COLORS["mregdc"], alpha=0.16)
    axes[3].set_xscale("log")
    axes[3].set_xlabel("ranked genes")
    axes[3].set_ylabel("-log10(adjusted P)")
    axes[3].set_title("ranked evidence decay", loc="left", fontweight="bold")
    axes[3].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[3])

    save_all(fig, "FigureS1_singleCellHaystack")


def draw_s2() -> None:
    hay = read_haystack()
    hs = read_hotspot()
    fig, axes = plt.subplots(2, 2, figsize=mm_fig(125), gridspec_kw={"wspace": 0.45, "hspace": 0.55})
    axes = axes.ravel()

    panel_label(axes[0], "A")
    lollipop(axes[0], hs, "Gene", "Z", COLORS["tls"], "Hotspot Z")
    axes[0].set_title("Hotspot top autocorrelation genes", loc="left", fontweight="bold")

    panel_label(axes[1], "B")
    axes[1].scatter(hs["C"], hs["Z"], s=8, color="#94A3B8", alpha=0.55, edgecolor="none")
    top = hs.sort_values("Z", ascending=False).head(8)
    axes[1].scatter(top["C"], top["Z"], s=20, color=COLORS["tls"], edgecolor="white", linewidth=0.35)
    annotate_ranked_points(axes[1], top, "C", "Z", "Gene", COLORS["tls"], n=6)
    axes[1].set_xlabel("Hotspot C")
    axes[1].set_ylabel("Hotspot Z")
    axes[1].set_title("autocorrelation strength", loc="left", fontweight="bold")
    axes[1].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[1])

    panel_label(axes[2], "C")
    ns = np.array([10, 25, 50, 100, 200, 500])
    overlaps = []
    for n in ns:
        set_hay = set(hay.sort_values("evidence", ascending=False).head(n)["Gene"])
        set_hs = set(hs.sort_values("Z", ascending=False).head(n)["Gene"])
        overlaps.append(len(set_hay.intersection(set_hs)))
    axes[2].plot(ns, overlaps, color=COLORS["green"], linewidth=1.6, marker="o", markersize=3.2)
    axes[2].set_xscale("log")
    axes[2].set_xlabel("top N genes per method")
    axes[2].set_ylabel("overlap count")
    axes[2].set_title("ranked-method overlap", loc="left", fontweight="bold")
    axes[2].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[2])

    panel_label(axes[3], "D")
    shared = list(
        set(hay.sort_values("evidence", ascending=False).head(80)["Gene"]).intersection(
            set(hs.sort_values("Z", ascending=False).head(80)["Gene"])
        )
    )
    if len(shared) < 8:
        shared = list(hs.sort_values("Z", ascending=False).head(12)["Gene"])
    comp = hay[hay["Gene"].isin(shared)][["Gene", "D_KL", "evidence"]].merge(
        hs[hs["Gene"].isin(shared)][["Gene", "C", "Z", "minus_log10_FDR"]],
        on="Gene",
        how="inner",
    )
    comp = comp.sort_values("Z", ascending=False).head(14).set_index("Gene")
    mat = zscore_frame(comp[["D_KL", "evidence", "C", "Z", "minus_log10_FDR"]])
    sns.heatmap(
        mat,
        ax=axes[3],
        cmap=DIVERGING_CMAP,
        center=0,
        cbar_kws={"label": "z", "shrink": 0.7},
        linewidths=0.55,
        linecolor="white",
    )
    axes[3].set_title("shared-gene evidence matrix", loc="left", fontweight="bold")
    axes[3].set_xlabel("")
    axes[3].set_ylabel("")
    style_heatmap_ax(axes[3])

    save_all(fig, "FigureS2_Hotspot")


def normalize_spatial_xy(df: pd.DataFrame, x_col: str = "x", y_col: str = "y") -> pd.DataFrame:
    out = df.copy()
    for src, dst in [(x_col, "x_plot"), (y_col, "y_plot")]:
        vals = pd.to_numeric(out[src], errors="coerce")
        span = vals.max(skipna=True) - vals.min(skipna=True)
        if not np.isfinite(span) or span == 0:
            out[dst] = 0.5
        else:
            out[dst] = (vals - vals.min(skipna=True)) / span
    return out


def spatial_base(
    ax: plt.Axes,
    df: pd.DataFrame,
    title: str,
    point_size: float = 1.2,
    alpha: float = 0.62,
    x_col: str = "x",
    y_col: str = "y",
    equal_aspect: bool = True,
    title_loc: str = "left",
) -> None:
    ax.scatter(df[x_col], df[y_col], s=point_size, color=COLORS["tissue"], alpha=alpha, edgecolor="none", rasterized=True)
    ax.set_title(title, loc=title_loc, fontweight="bold", pad=2)
    if equal_aspect:
        ax.set_aspect("equal", adjustable="box")
    else:
        ax.set_aspect("auto")
        ax.set_xlim(0, 1)
        ax.set_ylim(1, 0)
    ax.set_xticks([])
    ax.set_yticks([])
    if equal_aspect:
        ax.invert_yaxis()
    for spine in ax.spines.values():
        spine.set_linewidth(0.45)
        spine.set_color("#94A3B8")


def spatial_score(ax: plt.Axes, df: pd.DataFrame, value: str, title: str, cmap=SPATIAL_CMAP) -> mpl.collections.PathCollection:
    spatial_base(ax, df, title)
    vmin, vmax = quantile_limits(df[value])
    sc = ax.scatter(
        df["x"],
        df["y"],
        c=df[value],
        s=1.6,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        alpha=0.9,
        edgecolor="none",
        rasterized=True,
    )
    return sc


def smooth_field_contour(
    ax: plt.Axes,
    df: pd.DataFrame,
    value: str,
    color: str,
    quantile: float,
    linewidth: float,
    bins: int = 95,
) -> None:
    working = df[["x", "y", value]].dropna()
    if working.empty:
        return
    x = working["x"].to_numpy()
    y = working["y"].to_numpy()
    z = working[value].to_numpy()
    x_edges = np.linspace(np.nanmin(x), np.nanmax(x), bins + 1)
    y_edges = np.linspace(np.nanmin(y), np.nanmax(y), bins + 1)
    stat_sum, _, _ = np.histogram2d(y, x, bins=[y_edges, x_edges], weights=z)
    stat_n, _, _ = np.histogram2d(y, x, bins=[y_edges, x_edges])
    with np.errstate(invalid="ignore", divide="ignore"):
        grid = stat_sum / stat_n
    grid[stat_n == 0] = np.nan
    fill = np.nanmedian(grid)
    grid = np.where(np.isfinite(grid), grid, fill)
    try:
        from scipy.ndimage import gaussian_filter

        grid = gaussian_filter(grid, sigma=1.35)
    except Exception:
        pass
    level = np.nanquantile(grid, quantile)
    x_centers = (x_edges[:-1] + x_edges[1:]) / 2
    y_centers = (y_edges[:-1] + y_edges[1:]) / 2
    ax.contour(x_centers, y_centers, grid, levels=[level], colors=[color], linewidths=linewidth)


def draw_s3() -> None:
    spot = read_csv(
        SRC / "FigS04_multi_sample_spatial_source" / "multi_sample_spatial_extended_selected_map_spot_scores.csv"
    )
    for col in ["x", "y", "TLS_integrated_score", "mregDC_score", "AP_MHCII_score", "TLS_mregDC_cohigh", "TLS_integrated_z", "mregDC_z"]:
        spot[col] = pd.to_numeric(spot[col], errors="coerce")
    sample_key = (
        spot.groupby(["dataset", "sample_id"])["TLS_mregDC_cohigh"].mean().sort_values(ascending=False).index[0]
    )
    df = spot[(spot["dataset"] == sample_key[0]) & (spot["sample_id"] == sample_key[1])].copy()
    fig, axes = plt.subplots(2, 2, figsize=mm_fig(125), gridspec_kw={"wspace": 0.08, "hspace": 0.18})
    axes = axes.ravel()

    panel_label(axes[0], "A")
    sc = spatial_score(axes[0], df, "TLS_integrated_score", "TLS integrated")
    cb = fig.colorbar(sc, ax=axes[0], fraction=0.035, pad=0.01, label="score")
    cb.ax.tick_params(labelsize=6)
    cb.set_label("score", fontsize=7)

    panel_label(axes[1], "B")
    sc = spatial_score(axes[1], df, "mregDC_score", "mregDC axis")
    cb = fig.colorbar(sc, ax=axes[1], fraction=0.035, pad=0.01, label="score")
    cb.ax.tick_params(labelsize=6)
    cb.set_label("score", fontsize=7)

    panel_label(axes[2], "C")
    sc = spatial_score(axes[2], df, "AP_MHCII_score", "AP/MHC-II proxy")
    cb = fig.colorbar(sc, ax=axes[2], fraction=0.035, pad=0.01, label="score")
    cb.ax.tick_params(labelsize=6)
    cb.set_label("score", fontsize=7)

    panel_label(axes[3], "D")
    spatial_base(axes[3], df, "TLS/mregDC co-high field")
    tls_high = df["TLS_integrated_z"] >= df["TLS_integrated_z"].quantile(0.8)
    mreg_high = df["mregDC_z"] >= df["mregDC_z"].quantile(0.8)
    cohigh = df["TLS_mregDC_cohigh"] > 0
    axes[3].scatter(df.loc[tls_high, "x"], df.loc[tls_high, "y"], s=2.0, color=COLORS["tls"], alpha=0.22, edgecolor="none", rasterized=True)
    axes[3].scatter(df.loc[mreg_high, "x"], df.loc[mreg_high, "y"], s=2.0, color=COLORS["mregdc"], alpha=0.24, edgecolor="none", rasterized=True)
    axes[3].scatter(df.loc[cohigh, "x"], df.loc[cohigh, "y"], s=5.0, color=COLORS["cohigh"], alpha=0.95, edgecolor="white", linewidth=0.15, rasterized=True)
    smooth_field_contour(axes[3], df, "TLS_integrated_z", COLORS["green"], 0.82, 1.15)
    smooth_field_contour(axes[3], df, "mregDC_z", COLORS["tls"], 0.82, 1.05)
    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["cohigh"], markersize=4, label="co-high"),
        Line2D([0], [0], color=COLORS["green"], lw=1.0, label="TLS field"),
        Line2D([0], [0], color=COLORS["tls"], lw=1.0, label="mregDC field"),
    ]
    axes[3].legend(
        handles=handles,
        loc="lower left",
        frameon=True,
        framealpha=0.72,
        facecolor="white",
        edgecolor="none",
        handlelength=1.0,
        borderpad=0.15,
        labelspacing=0.2,
        fontsize=5,
    )

    save_all(fig, "FigureS3_spatial_core")


def draw_s4() -> None:
    spot = read_csv(
        SRC / "FigS04_multi_sample_spatial_source" / "multi_sample_spatial_extended_selected_map_spot_scores.csv"
    )
    sample_meta = read_csv(
        SRC / "FigS04_multi_sample_spatial_source" / "multi_sample_spatial_extended_selected_map_samples.csv"
    )
    sample_metrics = read_csv(
        SRC / "FigS04_multi_sample_spatial_source" / "multi_sample_spatial_extended_sample_metrics_long.csv"
    )
    dataset_summary = read_csv(
        SRC / "FigS04_multi_sample_spatial_source" / "multi_sample_spatial_extended_dataset_metric_summary.csv"
    )
    coverage = read_csv(
        SRC / "FigS04_multi_sample_spatial_source" / "multi_sample_spatial_extended_gene_coverage_fraction.csv"
    )
    for col in ["x", "y", "TLS_mregDC_cohigh"]:
        spot[col] = pd.to_numeric(spot[col], errors="coerce")
    for col in ["value"]:
        sample_metrics[col] = pd.to_numeric(sample_metrics[col], errors="coerce")
    dataset_summary["median_value"] = pd.to_numeric(dataset_summary["median_value"], errors="coerce")
    coverage["coverage_fraction"] = pd.to_numeric(coverage["coverage_fraction"], errors="coerce")
    dataset_label_map = dict(zip(sample_meta["dataset"], sample_meta["dataset_label"]))
    if "dataset_label" not in coverage.columns:
        coverage["dataset_label"] = coverage["dataset"].map(dataset_label_map).fillna(coverage["dataset"])

    fig = plt.figure(figsize=mm_fig(132))
    gs = GridSpec(2, 3, figure=fig, height_ratios=[0.86, 1.0], hspace=0.20, wspace=0.58)

    top = GridSpecFromSubplotSpec(1, 5, subplot_spec=gs[0, :], wspace=0.08)
    map_axes = [fig.add_subplot(top[0, i]) for i in range(5)]
    for i, (_, row) in enumerate(sample_meta.iterrows()):
        ax = map_axes[i]
        sub = spot[(spot["dataset"] == row["dataset"]) & (spot["sample_id"] == row["sample_id"])]
        spatial_base(
            ax,
            sub,
            str(row["dataset_label"]),
            point_size=1.8,
            alpha=0.78,
            x_col="x",
            y_col="y",
            equal_aspect=True,
            title_loc="left",
        )
        high = sub["TLS_mregDC_cohigh"] > 0
        ax.scatter(
            sub.loc[high, "x"],
            sub.loc[high, "y"],
            s=7.0,
            color=COLORS["cohigh"],
            alpha=0.92,
            edgecolor="white",
            linewidth=0.12,
            rasterized=True,
        )
        for spine in ax.spines.values():
            spine.set_color("#CBD5E1")
            spine.set_linewidth(0.45)
        if i == 0:
            panel_label(ax, "A")

    ax_b = fig.add_subplot(gs[1, 0])
    panel_label(ax_b, "B")
    metric_order = [
        "TLS/mregDC co-high O/E",
        "mregDC~TLS integrated",
        "mregDC~antigen-presentation/MHC-II",
        "TLS~antigen-presentation/MHC-II",
    ]
    ds_pivot = dataset_summary[dataset_summary["metric"].isin(metric_order)].pivot_table(
        index="dataset_label", columns="metric", values="median_value", aggfunc="median"
    )
    ds_pivot = ds_pivot[[m for m in metric_order if m in ds_pivot.columns]]
    ds_pivot = ds_pivot.rename(columns={c: short_metric_name(c) for c in ds_pivot.columns})
    ds_z = zscore_frame(ds_pivot)
    sns.heatmap(
        ds_z,
        ax=ax_b,
        cmap=DIVERGING_CMAP,
        center=0,
        linewidths=0.55,
        linecolor="white",
        cbar_kws={"label": "dataset z", "shrink": 0.65},
    )
    ax_b.set_title("dataset support", loc="left", fontweight="bold")
    ax_b.set_xlabel("")
    ax_b.set_ylabel("")
    style_heatmap_ax(ax_b)
    ax_b.tick_params(axis="x", labelrotation=0, labelsize=5.7, pad=1.2)
    ds_short = {
        "10x Visium": "Visium",
        "GSE211956": "G211956",
        "GSE224335": "G224335",
        "GSE274657": "G274657",
        "GSE288483": "G288483",
    }
    ax_b.set_yticklabels([ds_short.get(t.get_text(), t.get_text()) for t in ax_b.get_yticklabels()])
    ax_b.tick_params(axis="y", labelsize=5.5, pad=1.0)
    for label in ax_b.get_xticklabels():
        label.set_ha("center")

    ax_c = fig.add_subplot(gs[1, 1])
    panel_label(ax_c, "C")
    oe = sample_metrics[sample_metrics["metric"] == "TLS/mregDC co-high O/E"].copy()
    sns.stripplot(
        data=oe,
        x="value",
        y="dataset_label",
        hue="dataset_label",
        palette=DATASET_COLORS,
        ax=ax_c,
        size=3.5,
        jitter=0.08,
        legend=False,
    )
    sns.pointplot(
        data=oe,
        x="value",
        y="dataset_label",
        ax=ax_c,
        color="#111827",
        estimator="median",
        errorbar=("pi", 50),
        markers="|",
        linestyles="none",
    )
    ax_c.axvline(1.0, color="#94A3B8", linewidth=0.7, linestyle="--")
    ax_c.set_xlabel("observed/expected")
    ax_c.set_ylabel("")
    ax_c.set_yticklabels([])
    ax_c.set_title("co-high O/E", loc="left", fontweight="bold")
    ax_c.grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=ax_c, left=True)

    ax_d = fig.add_subplot(gs[1, 2])
    panel_label(ax_d, "D")
    cov = coverage.pivot_table(index="dataset_label", columns="signature", values="coverage_fraction", aggfunc="median")
    cov = cov.loc[[idx for idx in DATASET_COLORS if idx in cov.index]]
    cov = cov.rename(columns={c: short_signature(c) for c in cov.columns})
    sns.heatmap(
        cov,
        ax=ax_d,
        cmap=LinearSegmentedColormap.from_list("coverage", ["#F8FAFC", "#7DD3FC", "#075985"]),
        vmin=0,
        vmax=1,
        linewidths=0.55,
        linecolor="white",
        cbar_kws={"label": "coverage", "shrink": 0.65},
    )
    ax_d.set_title("gene coverage", loc="left", fontweight="bold")
    ax_d.set_xlabel("")
    ax_d.set_ylabel("")
    ax_d.set_yticklabels([])
    style_heatmap_ax(ax_d)
    ax_d.tick_params(axis="x", labelrotation=34, labelsize=5.3, pad=1.0)

    fig.subplots_adjust(left=0.085, right=0.985, top=0.935, bottom=0.095)
    save_all(fig, "FigureS4_multi_sample_spatial_validation")


def draw_s5() -> None:
    cv = read_csv(SRC / "FigS05_model_validation" / "source_LASSO_CV_curve.csv")
    coef = read_csv(SRC / "FigS05_model_validation" / "source_LASSO_lambda_min_coefficients.csv")
    auc = read_csv(SRC / "FigS05_model_validation" / "source_time_dependent_ROC_AUC.csv")
    roc = read_csv(SRC / "FigS05_model_validation" / "source_time_dependent_ROC_curve.csv")
    cal = read_csv(SRC / "FigS05_model_validation" / "source_calibration_by_quintile.csv")
    for frame in [cv, coef, auc, roc, cal]:
        for col in frame.columns:
            if col not in ["feature", "time_label"]:
                frame[col] = pd.to_numeric(frame[col], errors="coerce")

    fig, axes = plt.subplots(2, 2, figsize=mm_fig(125), gridspec_kw={"wspace": 0.42, "hspace": 0.55})
    axes = axes.ravel()

    panel_label(axes[0], "A")
    axes[0].plot(cv["log_lambda"], cv["cvm"], color="#111827", linewidth=1.2)
    axes[0].fill_between(cv["log_lambda"], cv["cvlo"], cv["cvup"], color="#94A3B8", alpha=0.25, linewidth=0)
    for lam, color, label in [
        (cv["lambda_min"].iloc[0], COLORS["cohigh"], "lambda.min"),
        (cv["lambda_1se"].iloc[0], COLORS["grey"], "lambda.1se"),
    ]:
        axes[0].axvline(np.log(lam), color=color, linewidth=0.8, linestyle="--", label=label)
    axes[0].set_xlabel("log(lambda)")
    axes[0].set_ylabel("cross-validated error")
    axes[0].set_title("LASSO cross-validation", loc="left", fontweight="bold")
    axes[0].legend(frameon=False)
    axes[0].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[0])

    panel_label(axes[1], "B")
    coef["abs_coef"] = coef["coefficient_lambda_min"].abs()
    plot_coef = coef.sort_values("abs_coef", ascending=True)
    y = np.arange(plot_coef.shape[0])
    colors = np.where(plot_coef["coefficient_lambda_min"] >= 0, COLORS["risk"], COLORS["green"])
    axes[1].axvline(0, color="#94A3B8", linewidth=0.7)
    axes[1].hlines(y, 0, plot_coef["coefficient_lambda_min"], color="#CBD5E1", linewidth=1.0)
    axes[1].scatter(plot_coef["coefficient_lambda_min"], y, c=colors, s=22, edgecolor="white", linewidth=0.35)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels([clean_label(x, 22) for x in plot_coef["feature"]])
    axes[1].set_xlabel("coefficient")
    axes[1].set_title("lambda.min coefficients", loc="left", fontweight="bold")
    axes[1].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[1], left=True)

    panel_label(axes[2], "C")
    roc_colors = {"1 year": COLORS["grey"], "3 years": COLORS["ap"], "5 years": COLORS["cohigh"]}
    for time_label, group in roc.groupby("time_label", sort=False):
        label_auc = auc.loc[auc["time_label"] == time_label, "AUC"]
        label = f"{time_label} AUC={label_auc.iloc[0]:.2f}" if not label_auc.empty else str(time_label)
        axes[2].plot(group["FP"], group["TP"], linewidth=1.4, color=roc_colors.get(time_label, COLORS["tls"]), label=label)
    axes[2].plot([0, 1], [0, 1], color="#CBD5E1", linewidth=0.8, linestyle="--")
    axes[2].set_xlabel("1 - specificity")
    axes[2].set_ylabel("sensitivity")
    axes[2].set_title("time-dependent ROC", loc="left", fontweight="bold")
    axes[2].legend(frameon=False, loc="lower right")
    axes[2].set_xlim(0, 1)
    axes[2].set_ylim(0, 1)
    sns.despine(ax=axes[2])

    panel_label(axes[3], "D")
    for time_label, group in cal.groupby("time_label", sort=False):
        color = roc_colors.get(time_label, COLORS["tls"])
        axes[3].errorbar(
            group["predicted_survival"],
            group["observed_survival"],
            yerr=[
                group["observed_survival"] - group["observed_lower95"],
                group["observed_upper95"] - group["observed_survival"],
            ],
            fmt="o-",
            markersize=3,
            linewidth=1.0,
            color=color,
            capsize=1.5,
            label=time_label,
        )
    axes[3].plot([0, 1], [0, 1], color="#CBD5E1", linewidth=0.8, linestyle="--")
    axes[3].set_xlabel("predicted survival")
    axes[3].set_ylabel("observed survival")
    axes[3].set_xlim(0.55, 1.0)
    axes[3].set_ylim(0.55, 1.0)
    axes[3].set_title("calibration by risk quintile", loc="left", fontweight="bold")
    axes[3].legend(frameon=False)
    axes[3].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[3])

    save_all(fig, "FigureS5_model_validation")


def relation_short(label: str) -> str:
    text = str(label)
    dataset_prefix = ""
    if ":" in text and text.split(":", 1)[0].startswith(("10x", "GSE")):
        prefix, text = text.split(":", 1)
        dataset_prefix = "10x" if prefix.startswith("10x") else prefix
    if "mregDC vs TLS" in text:
        base = "mregDC-TLS"
    elif "mregDC vs AP/MHC-II" in text:
        base = "mregDC-AP"
    elif "TLS vs AP/MHC-II" in text:
        base = "TLS-AP"
    elif "axis vs AP/MHC-II" in text:
        base = "axis-AP"
    elif "axis vs B follicle" in text:
        base = "axis-B"
    elif "axis vs T zone" in text:
        base = "axis-T"
    else:
        base = text.split("|")[0].strip()
    suffix = ""
    if "APC/myeloid" in text:
        suffix = "\n+APC"
    elif "spot controls" in text:
        suffix = "\nspot"
    elif "core controls" in text:
        suffix = "\ncore"
    elif "Xenium" in str(label):
        suffix = "\nadj"
    if dataset_prefix:
        return f"{dataset_prefix} {base}"
    return base + suffix


def relation_base(label: str) -> str:
    text = str(label)
    if "mregDC vs TLS" in text:
        return "mregDC-TLS"
    if "mregDC vs AP/MHC-II" in text:
        return "mregDC-AP"
    if "TLS vs AP/MHC-II" in text:
        return "TLS-AP"
    if "axis vs AP/MHC-II" in text:
        return "axis-AP"
    if "axis vs B follicle" in text:
        return "axis-B"
    if "axis vs T zone" in text:
        return "axis-T"
    return text.split("|")[0].strip()


def draw_s6() -> None:
    pc = read_csv(SRC / "FigS06_specificity_adjustment" / "partial_correlation_results_combined.csv")
    reg = read_csv(SRC / "FigS06_specificity_adjustment" / "tcga_adjusted_regression_results.csv")
    controls = read_csv(SRC / "FigS06_specificity_adjustment" / "immune_control_definitions.csv")
    for frame in [pc, reg]:
        for col in frame.columns:
            if col not in ["layer", "label", "x", "y", "controls", "status", "outcome", "predictor"]:
                frame[col] = pd.to_numeric(frame[col], errors="coerce")
    pc = pc[pc["status"] == "ok"].copy()
    reg = reg[reg["status"] == "ok"].copy()
    pc["short"] = pc["label"].map(relation_short)
    pc["base"] = pc["label"].map(relation_base)
    pc["layer_short"] = pc["layer"].map(short_layer_name)
    reg["short"] = reg["label"].map(relation_short)

    fig, axes = plt.subplots(2, 2, figsize=mm_fig(125), gridspec_kw={"wspace": 0.5, "hspace": 0.55})
    axes = axes.ravel()

    panel_label(axes[0], "A")
    key = pc[
        (pc["layer"] == "TCGA patient")
        & (pc["label"].str.contains("mregDC vs TLS|mregDC vs AP/MHC-II|TLS vs AP/MHC-II"))
    ].copy()
    key = key.head(6)
    y = np.arange(key.shape[0])
    axes[0].hlines(y, key["raw_spearman_rho"], key["partial_spearman_rho"], color="#CBD5E1", linewidth=1.0)
    axes[0].scatter(key["raw_spearman_rho"], y, s=18, color="#94A3B8", label="raw", zorder=2)
    axes[0].scatter(key["partial_spearman_rho"], y, s=20, color=COLORS["cohigh"], label="partial", zorder=3)
    axes[0].axvline(0, color="#94A3B8", linewidth=0.7)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(key["short"])
    axes[0].set_xlabel("Spearman rho")
    axes[0].set_title("raw versus adjusted association", loc="left", fontweight="bold")
    axes[0].legend(frameon=False, loc="lower right")
    axes[0].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[0], left=True)

    panel_label(axes[1], "B")
    heat_source = pc[
        pc["label"].str.contains("mregDC vs TLS|mregDC vs AP/MHC-II|TLS vs AP/MHC-II")
    ].copy()
    heat = heat_source.pivot_table(index="base", columns="layer_short", values="partial_spearman_rho", aggfunc="median")
    heat = heat.reindex(["mregDC-TLS", "mregDC-AP", "TLS-AP"])
    sns.heatmap(
        heat,
        ax=axes[1],
        cmap=DIVERGING_CMAP,
        center=0,
        vmin=-0.35,
        vmax=0.35,
        linewidths=0.55,
        linecolor="white",
        cbar_kws={"label": "partial rho", "shrink": 0.7},
    )
    axes[1].set_title("adjusted-correlation matrix", loc="left", fontweight="bold")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("")
    style_heatmap_ax(axes[1])

    panel_label(axes[2], "C")
    forest = reg[
        reg["label"].str.contains("mregDC vs TLS|mregDC vs AP/MHC-II|TLS vs AP/MHC-II")
    ].copy().head(6).iloc[::-1]
    forest["lo"] = forest["beta"] - 1.96 * forest["se_hc3"]
    forest["hi"] = forest["beta"] + 1.96 * forest["se_hc3"]
    y = np.arange(forest.shape[0])
    axes[2].axvline(0, color="#94A3B8", linewidth=0.7)
    axes[2].hlines(y, forest["lo"], forest["hi"], color="#CBD5E1", linewidth=1.0)
    axes[2].scatter(forest["beta"], y, s=22, color=COLORS["ap"], edgecolor="white", linewidth=0.35)
    axes[2].set_yticks(y)
    axes[2].set_yticklabels(forest["short"])
    axes[2].set_xlabel("adjusted beta (HC3 95% CI)")
    axes[2].set_title("adjusted regression support", loc="left", fontweight="bold")
    axes[2].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[2], left=True)

    panel_label(axes[3], "D")
    reg["n_controls"] = reg["controls"].fillna("").apply(lambda s: 0 if not s else len(str(s).split(";")))
    summary = reg[
        reg["label"].str.contains("mregDC vs TLS|mregDC vs AP/MHC-II|TLS vs AP/MHC-II")
    ].copy()
    summary = summary.groupby("short").agg(n=("n", "median"), controls=("n_controls", "median"), adj_r2=("adj_r2", "median")).reset_index()
    summary = summary.sort_values("adj_r2", ascending=True)
    y = np.arange(summary.shape[0])
    axes[3].barh(y, summary["adj_r2"], color="#E2E8F0", edgecolor="white", height=0.7, label="adj. R2")
    axes[3].scatter(summary["controls"] / max(summary["controls"].max(), 1), y, s=30, color=COLORS["green"], zorder=3, label="controls")
    axes[3].set_yticks(y)
    axes[3].set_yticklabels(summary["short"])
    axes[3].set_xlabel("adjusted R2")
    axes[3].set_title("model-control summary", loc="left", fontweight="bold")
    axes[3].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    axes[3].legend(frameon=False, loc="lower right")
    sns.despine(ax=axes[3], left=True)

    save_all(fig, "FigureS6_specificity_adjusted_associations")


def draw_s7() -> None:
    mat = read_csv(SRC / "FigS07_drug_prioritization_docking" / "FigS07_CH_drug_vulnerability_matrix_source_matrix.csv")
    scores = read_csv(
        SRC / "FigS07_drug_prioritization_docking" / "FigS07_drug_prioritization_derived_scores.tsv",
        sep="\t",
    )
    for frame in [mat, scores]:
        for col in frame.columns:
            if col not in ["feature", "compound", "target_class"]:
                frame[col] = pd.to_numeric(frame[col], errors="coerce")
    fig, axes = plt.subplots(2, 2, figsize=mm_fig(125), gridspec_kw={"wspace": 0.45, "hspace": 0.55})
    axes = axes.ravel()

    panel_label(axes[0], "A")
    matrix = mat.set_index("feature")
    matrix = matrix.rename(
        columns={
            "target direct": "target",
            "virtual screen": "screen",
            "risk reversal": "risk",
            "TLS suppression": "TLS",
            "axis suppression": "axis",
            "IF suppression": "IF",
            "AP suppression": "AP",
        }
    )
    sns.heatmap(
        matrix,
        ax=axes[0],
        cmap=PRIORITY_CMAP,
        center=0,
        linewidths=0.45,
        linecolor="white",
        cbar_kws={"label": "z", "shrink": 0.7},
    )
    axes[0].set_title("drug evidence matrix", loc="left", fontweight="bold")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("")
    style_heatmap_ax(axes[0])
    axes[0].tick_params(axis="x", labelrotation=45)

    panel_label(axes[1], "B")
    rank = scores.sort_values("mean_priority", ascending=True)
    y = np.arange(rank.shape[0])
    axes[1].hlines(y, 0, rank["mean_priority"], color="#CBD5E1", linewidth=1.0)
    class_palette = dict(zip(rank["target_class"].unique(), sns.color_palette("Set2", n_colors=rank["target_class"].nunique()).as_hex()))
    axes[1].scatter(rank["mean_priority"], y, s=24, c=rank["target_class"].map(class_palette), edgecolor="white", linewidth=0.35)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(rank["compound"])
    axes[1].set_xlabel("mean priority z")
    axes[1].set_title("integrated priority ranking", loc="left", fontweight="bold")
    axes[1].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[1], left=True)

    panel_label(axes[2], "C")
    scatter = axes[2].scatter(
        scores["target_evidence"],
        scores["program_reversal"],
        c=scores["docking_support"],
        s=45 + 35 * (scores["mean_priority"] - scores["mean_priority"].min()) / (scores["mean_priority"].max() - scores["mean_priority"].min() + 1e-9),
        cmap=DIVERGING_CMAP,
        norm=TwoSlopeNorm(vcenter=0, vmin=scores["docking_support"].min(), vmax=scores["docking_support"].max()),
        edgecolor="white",
        linewidth=0.35,
    )
    priority_top = scores.sort_values("mean_priority", ascending=False).head(4)
    annotate_ranked_points(axes[2], priority_top, "target_evidence", "program_reversal", "compound", COLORS["cohigh"], n=4)
    axes[2].set_xlabel("target evidence")
    axes[2].set_ylabel("program reversal")
    axes[2].set_title("mechanism-evidence plane", loc="left", fontweight="bold")
    fig.colorbar(scatter, ax=axes[2], fraction=0.04, pad=0.02, label="docking")
    axes[2].grid(color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[2])

    panel_label(axes[3], "D")
    order = scores.groupby("target_class")["mean_priority"].median().sort_values().index
    sns.boxplot(data=scores, y="target_class", x="mean_priority", order=order, ax=axes[3], color="#E2E8F0", width=0.55, fliersize=0)
    sns.stripplot(data=scores, y="target_class", x="mean_priority", order=order, ax=axes[3], hue="target_class", palette=class_palette, size=4, jitter=0.12, legend=False)
    axes[3].axvline(0, color="#94A3B8", linewidth=0.7, linestyle="--")
    axes[3].set_xlabel("mean priority z")
    axes[3].set_ylabel("")
    axes[3].set_title("priority by target class", loc="left", fontweight="bold")
    axes[3].grid(axis="x", color="#E5E7EB", linewidth=0.45)
    sns.despine(ax=axes[3], left=True)

    save_all(fig, "Supplementary_Figure_S7_drug_prioritization")


def build_contact_sheet() -> None:
    files = [
        EXPORT / "FigureS1_singleCellHaystack.png",
        EXPORT / "FigureS2_Hotspot.png",
        EXPORT / "FigureS3_spatial_core.png",
        EXPORT / "FigureS4_multi_sample_spatial_validation.png",
        EXPORT / "FigureS5_model_validation.png",
        EXPORT / "FigureS6_specificity_adjusted_associations.png",
        EXPORT / "Supplementary_Figure_S7_drug_prioritization.png",
    ]
    thumbs = []
    for path in files:
        img = Image.open(path).convert("RGB")
        img.thumbnail((900, 640), Image.Resampling.LANCZOS)
        thumbs.append((path.stem, img.copy()))
    pad = 40
    label_h = 26
    w = 2 * 900 + 3 * pad
    h = 4 * (640 + label_h) + 5 * pad
    sheet = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
    for i, (name, img) in enumerate(thumbs):
        row = i // 2
        col = i % 2
        x = pad + col * (900 + pad)
        y = pad + row * (640 + label_h + pad)
        draw.text((x, y), name, fill=(17, 24, 39), font=font)
        sheet.paste(img, (x, y + label_h))
    sheet.save(QC / "SUP_CNS_v2_contact_sheet.png", quality=95)


def write_render_manifest() -> None:
    records = []
    for path in sorted(EXPORT.glob("*")):
        if path.suffix.lower() in [".png", ".pdf", ".svg"]:
            records.append(
                {
                    "file": path.name,
                    "bytes": path.stat().st_size,
                    "suffix": path.suffix.lower(),
                }
            )
    pd.DataFrame(records).to_csv(QC / "render_manifest.csv", index=False)


def main() -> None:
    setup_style()
    draw_s1()
    draw_s2()
    draw_s3()
    draw_s4()
    draw_s5()
    draw_s6()
    draw_s7()
    build_contact_sheet()
    write_render_manifest()


if __name__ == "__main__":
    main()
