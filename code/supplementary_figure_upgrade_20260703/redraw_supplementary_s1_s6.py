from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


ROOT = Path("/mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629")
SRC = ROOT / "07_submission_package_R1" / "_source_data_stage"
OUT = ROOT / "08_supplementary_figure_upgrade_20260702" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 7.5,
        "axes.titlesize": 9.5,
        "axes.titleweight": "bold",
        "axes.labelsize": 8,
        "axes.linewidth": 0.6,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "legend.title_fontsize": 7.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

PAL = {
    "mregDC/AP": "#D63C79",
    "AP/MHC-II proxy": "#3B73B9",
    "TLS lymphoid": "#42A66A",
    "IF/core": "#E6A532",
    "raw": "#9CA3AF",
    "adjusted": "#D63C79",
}
DATASET_COLS = {
    "10x Visium": "#C8A200",
    "GSE211956": "#2F65C8",
    "GSE224335": "#11A6AE",
    "GSE274657": "#DF3B78",
    "GSE288483": "#2FA463",
}
METRIC_ORDER = [
    "mregDC~TLS integrated",
    "mregDC~TLS 12CK",
    "mregDC~TLS imprint",
    "mregDC~antigen-presentation/MHC-II",
    "TLS~antigen-presentation/MHC-II",
    "TLS/mregDC co-high O/E",
]
METRIC_LABELS = {
    "mregDC~TLS integrated": "mregDC~TLS",
    "mregDC~TLS 12CK": "12CK",
    "mregDC~TLS imprint": "TLS imprint",
    "mregDC~antigen-presentation/MHC-II": "mregDC~AP",
    "TLS~antigen-presentation/MHC-II": "TLS~AP",
    "TLS/mregDC co-high O/E": "co-high O/E",
}


def mm_to_in(mm: float) -> float:
    return mm / 25.4


def clean_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(width=0.5, length=2.2, colors="#202833")
    ax.grid(axis="x", color="#E5E7EB", linewidth=0.5)
    ax.set_axisbelow(True)


def add_panel_label(ax, label: str):
    ax.text(
        -0.12,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
        va="top",
        ha="left",
        color="black",
    )


def save_fig(fig, stem: str, width_mm: float, height_mm: float):
    fig.set_size_inches(mm_to_in(width_mm), mm_to_in(height_mm))
    fig.savefig(OUT / f"{stem}.svg", facecolor="white")
    fig.savefig(OUT / f"{stem}.pdf", facecolor="white")
    fig.savefig(OUT / f"{stem}.png", dpi=600, facecolor="white")
    fig.savefig(OUT / f"{stem}.tiff", dpi=600, facecolor="white")
    plt.close(fig)


MARKER_GROUPS = {
    "mregDC/AP": [
        "LAMP3",
        "CCR7",
        "CD40",
        "CD80",
        "CD86",
        "CD274",
        "PDCD1LG2",
        "FSCN1",
        "BIRC3",
        "NFKBIA",
        "CCL19",
        "CCL22",
    ],
    "AP/MHC-II proxy": [
        "CD74",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
        "CIITA",
        "TAP1",
        "TAP2",
        "B2M",
    ],
    "TLS lymphoid": [
        "CXCL13",
        "CCL19",
        "CCL21",
        "CXCL9",
        "CXCL10",
        "CXCL11",
        "MS4A1",
        "CD79A",
        "CD3D",
        "CD3E",
    ],
}


def selected_marker_table(df: pd.DataFrame, gene_col: str, score_col: str) -> pd.DataFrame:
    ranked = df.sort_values(score_col, ascending=False).reset_index(drop=True).copy()
    ranked["rank"] = np.arange(1, ranked.shape[0] + 1)
    rows = []
    for group, genes in MARKER_GROUPS.items():
        sub = ranked[ranked[gene_col].isin(genes)].copy()
        if sub.empty:
            continue
        sub["group"] = group
        rows.append(sub[[gene_col, score_col, "rank", "group"]])
    out = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=[gene_col, score_col, "rank", "group"])
    out = out.sort_values(["group", score_col], ascending=[True, False])
    return out


def draw_rank_audit(rank_df: pd.DataFrame, gene_col: str, score_col: str, top_title: str, x_label: str, out_stem: str):
    fig, axes = plt.subplots(
        1,
        2,
        gridspec_kw={"width_ratios": [1.03, 1.15], "wspace": 0.55},
        constrained_layout=False,
    )
    top = rank_df.sort_values(score_col, ascending=False).head(16).iloc[::-1]
    axes[0].barh(top[gene_col], top[score_col], color="#D63C79", alpha=0.85, height=0.68)
    axes[0].set_title("Top ranked genes", loc="left")
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel("")
    clean_axis(axes[0])
    add_panel_label(axes[0], "A")

    audit = selected_marker_table(rank_df, gene_col, score_col)
    audit = audit.groupby("group", group_keys=False).head(8).copy()
    audit = audit.sort_values(score_col)
    y = np.arange(audit.shape[0])
    axes[1].hlines(y, 0, audit[score_col], color="#D1D5DB", linewidth=0.8)
    for group, sub in audit.groupby("group", sort=False):
        axes[1].scatter(
            sub[score_col],
            [audit.index.get_loc(idx) for idx in sub.index],
            s=np.clip(70 - sub["rank"] / 40, 18, 60),
            color=PAL.get(group, "#4B5563"),
            label=group,
            edgecolor="white",
            linewidth=0.35,
            zorder=3,
        )
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(audit[gene_col])
    axes[1].set_title("TLS/mregDC marker audit", loc="left")
    axes[1].set_xlabel(x_label)
    axes[1].set_ylabel("")
    axes[1].legend(frameon=False, loc="lower right")
    clean_axis(axes[1])
    add_panel_label(axes[1], "B")
    fig.suptitle(top_title, x=0.02, ha="left", y=0.975, fontsize=9.8, fontweight="bold")
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.18, top=0.76, wspace=0.58)
    save_fig(fig, out_stem, 180, 78)


def redraw_s1_s2():
    s1 = pd.read_csv(SRC / "FigS01_singleCellHaystack_audit" / "SourceData_FigS1_singleCellHaystack_ranked_features.tsv", sep="\t")
    draw_rank_audit(
        s1,
        gene_col="gene",
        score_col="D_KL",
        top_title="singleCellHaystack spatial non-randomness audit",
        x_label="D_KL evidence",
        out_stem="FigureS1_singleCellHaystack_redraw",
    )

    s2 = pd.read_csv(SRC / "FigS02_Hotspot_audit" / "SourceData_FigS2_Hotspot_autocorrelations.tsv", sep="\t")
    draw_rank_audit(
        s2,
        gene_col="Gene",
        score_col="Z",
        top_title="Hotspot spatial-autocorrelation audit",
        x_label="Hotspot Z",
        out_stem="FigureS2_Hotspot_redraw",
    )


def redraw_s4():
    s4 = SRC / "FigS04_multi_sample_spatial_source"
    metrics = pd.read_csv(s4 / "multi_sample_spatial_extended_dataset_metric_summary.csv")
    coverage = pd.read_csv(s4 / "multi_sample_spatial_extended_gene_coverage_fraction.csv")
    avail = pd.read_csv(s4 / "multi_sample_spatial_extended_exact_marker_availability.csv")
    if "dataset_label" not in coverage.columns:
        coverage["dataset_label"] = coverage["dataset"].replace(
            {"10x_human_ovarian_cancer_ffpe_visium": "10x Visium"}
        )

    fig = plt.figure()
    gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1.0], width_ratios=[1.35, 0.75], hspace=0.72, wspace=0.42)
    axes = [fig.add_subplot(gs[0, :]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])]

    m = metrics[metrics["metric"].isin(METRIC_ORDER)].copy()
    m["metric_label"] = m["metric"].map(METRIC_LABELS)
    m["dataset_label"] = pd.Categorical(m["dataset_label"], categories=list(DATASET_COLS), ordered=True)
    m["metric_label"] = pd.Categorical(m["metric_label"], categories=[METRIC_LABELS[x] for x in METRIC_ORDER], ordered=True)
    piv = m.pivot_table(index="dataset_label", columns="metric_label", values="median_value", observed=False)
    sns.heatmap(
        piv,
        ax=axes[0],
        cmap=sns.diverging_palette(240, 10, as_cmap=True),
        center=0,
        linewidths=0.6,
        linecolor="white",
        cbar_kws={"label": "median"},
    )
    axes[0].set_title("Dataset-level spatial support", loc="left")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("")
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].tick_params(axis="y", rotation=0)
    add_panel_label(axes[0], "A")

    cov = coverage.copy()
    cov_summary = cov.groupby(["dataset_label", "signature"], as_index=False)["coverage_fraction"].mean()
    sig_order = ["TLS_12CK", "TLS_29_imprint", "mregDC", "AP_MHCII", "B_cell_TLS", "T_cell_zone"]
    cov_summary = cov_summary[cov_summary["signature"].isin(sig_order)]
    cov_summary["dataset_label"] = pd.Categorical(cov_summary["dataset_label"], categories=list(DATASET_COLS), ordered=True)
    cov_summary["signature"] = pd.Categorical(cov_summary["signature"], categories=sig_order, ordered=True)
    cov_piv = cov_summary.pivot_table(index="dataset_label", columns="signature", values="coverage_fraction", observed=False)
    sns.heatmap(
        cov_piv,
        ax=axes[1],
        cmap="YlGnBu",
        vmin=0,
        vmax=1,
        linewidths=0.6,
        linecolor="white",
        cbar_kws={"label": "gene coverage"},
    )
    axes[1].set_title("Signature gene coverage", loc="left")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("")
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].tick_params(axis="y", rotation=0)
    add_panel_label(axes[1], "B")

    av = avail.copy()
    av_summary = av.groupby(["dataset_label", "marker"], as_index=False)["available"].mean()
    av_summary["dataset_label"] = pd.Categorical(av_summary["dataset_label"], categories=list(DATASET_COLS), ordered=True)
    av_summary["marker"] = pd.Categorical(av_summary["marker"], categories=["HLA-DRA", "LAMP3", "CCR7"], ordered=True)
    av_piv = av_summary.pivot_table(index="dataset_label", columns="marker", values="available", observed=False)
    sns.heatmap(
        av_piv,
        ax=axes[2],
        cmap=sns.light_palette("#D63C79", as_cmap=True),
        vmin=0,
        vmax=1,
        linewidths=0.6,
        linecolor="white",
        cbar_kws={"label": "fraction"},
    )
    axes[2].set_title("Exact markers", loc="left")
    axes[2].set_xlabel("")
    axes[2].set_ylabel("")
    axes[2].tick_params(axis="x", rotation=45)
    axes[2].tick_params(axis="y", rotation=0)
    add_panel_label(axes[2], "C")
    fig.subplots_adjust(left=0.13, right=0.98, bottom=0.18, top=0.9)
    save_fig(fig, "FigureS4_multi_sample_spatial_validation_redraw", 180, 105)


def redraw_s5():
    s5 = SRC / "FigS05_model_validation"
    roc = pd.read_csv(s5 / "source_time_dependent_ROC_curve.csv")
    auc = pd.read_csv(s5 / "source_time_dependent_ROC_AUC.csv")
    cv = pd.read_csv(s5 / "source_LASSO_CV_curve.csv")
    cal = pd.read_csv(s5 / "source_calibration_by_quintile.csv")

    time_cols = {"1 year": "#3B73B9", "3 years": "#D63C79", "5 years": "#42A66A"}
    fig, axes = plt.subplots(1, 3, gridspec_kw={"width_ratios": [1, 1, 1.08], "wspace": 0.48})

    for label, sub in roc.groupby("time_label"):
        auc_val = auc.loc[auc["time_label"] == label, "AUC"].iloc[0]
        axes[0].plot(sub["FP"], sub["TP"], lw=1.6, color=time_cols.get(label), label=f"{label} AUC={auc_val:.2f}")
    axes[0].plot([0, 1], [0, 1], ls="--", lw=0.7, color="#9CA3AF")
    axes[0].set_title("ROC", loc="left")
    axes[0].set_xlabel("False-positive rate")
    axes[0].set_ylabel("True-positive rate")
    axes[0].legend(frameon=False, loc="lower right")
    clean_axis(axes[0])
    add_panel_label(axes[0], "A")

    axes[1].plot(cv["log_lambda"], cv["cvm"], color="#202833", lw=1.4)
    axes[1].fill_between(cv["log_lambda"], cv["cvlo"], cv["cvup"], color="#BFC7D5", alpha=0.45, linewidth=0)
    axes[1].axvline(np.log(cv["lambda_min"].iloc[0]), color="#D63C79", lw=1.0, ls="--", label="lambda.min")
    axes[1].axvline(np.log(cv["lambda_1se"].iloc[0]), color="#3B73B9", lw=1.0, ls=":", label="lambda.1se")
    axes[1].set_title("LASSO-Cox CV", loc="left")
    axes[1].set_xlabel("log(lambda)")
    axes[1].set_ylabel("CV partial likelihood deviance")
    axes[1].legend(frameon=False, loc="upper left")
    clean_axis(axes[1])
    add_panel_label(axes[1], "B")

    for label, sub in cal.groupby("time_label"):
        sub = sub.sort_values("predicted_survival")
        axes[2].errorbar(
            sub["predicted_survival"],
            sub["observed_survival"],
            yerr=[sub["observed_survival"] - sub["observed_lower95"], sub["observed_upper95"] - sub["observed_survival"]],
            marker="o",
            ms=3.2,
            lw=1.1,
            capsize=2,
            color=time_cols.get(label),
            label=label,
        )
    axes[2].plot([0, 1], [0, 1], ls="--", lw=0.7, color="#9CA3AF")
    axes[2].set_xlim(0.25, 1.0)
    axes[2].set_ylim(0.25, 1.03)
    axes[2].set_title("Calibration", loc="left")
    axes[2].set_xlabel("Predicted survival")
    axes[2].set_ylabel("Observed survival")
    axes[2].legend(frameon=False, loc="lower right")
    clean_axis(axes[2])
    add_panel_label(axes[2], "C")
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.16, top=0.86, wspace=0.48)
    save_fig(fig, "FigureS5_model_validation_redraw", 180, 75)


def redraw_s6():
    df = pd.read_csv(SRC / "FigS06_specificity_adjustment" / "specificity_compact_plot_values.csv")
    panels = ["TCGA-OV patients", "Spatial spots", "Xenium cells"]
    rel_order = ["mregDC-TLS", "mregDC-AP/MHC-II", "TLS-AP/MHC-II"]
    fig, axes = plt.subplots(1, 3, sharey=False, gridspec_kw={"wspace": 0.28})
    for i, panel in enumerate(panels):
        ax = axes[i]
        sub = df[df["panel"] == panel].copy()
        sub["relation"] = pd.Categorical(sub["relation"], categories=rel_order[::-1], ordered=True)
        sub = sub.sort_values("relation")
        y = np.arange(sub.shape[0])
        for yi, row in zip(y, sub.itertuples()):
            ax.plot([row.raw, row.adjusted], [yi, yi], color="#D1D5DB", lw=1.2, zorder=1)
        ax.scatter(sub["raw"], y, color=PAL["raw"], s=36, label="raw" if i == 0 else None, zorder=2)
        ax.scatter(sub["adjusted"], y, color=PAL["adjusted"], s=42, label="adjusted" if i == 0 else None, zorder=3)
        ax.axvline(0, color="#6B7280", lw=0.65, ls="--")
        ax.set_title(panel, loc="left")
        ax.set_xlabel("Spearman rho")
        ax.set_yticks(y)
        if i == 0:
            ax.set_yticklabels(list(sub["relation"]))
        else:
            ax.set_yticklabels([])
        ax.set_ylabel("")
        add_panel_label(ax, chr(ord("A") + i))
        ax.set_xlim(-0.18, 0.9)
        clean_axis(ax)
    axes[0].legend(frameon=False, loc="lower right")
    fig.subplots_adjust(left=0.2, right=0.98, bottom=0.22, top=0.84, wspace=0.28)
    save_fig(fig, "FigureS6_specificity_adjusted_associations_redraw", 180, 62)


def main():
    redraw_s1_s2()
    redraw_s4()
    redraw_s5()
    redraw_s6()


if __name__ == "__main__":
    main()
