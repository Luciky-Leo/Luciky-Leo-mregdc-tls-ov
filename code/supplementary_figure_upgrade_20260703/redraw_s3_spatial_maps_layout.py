from __future__ import annotations

from pathlib import Path

import fitz
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


ROOT = Path("/mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629")
SRC_PDF = ROOT / "07_submission_package_R1" / "_source_data_stage" / "FigS03_Xenium_spatial_maps" / "FigureS3_Xenium_spatial_maps-re.pdf"
OUT = ROOT / "08_supplementary_figure_upgrade_20260702" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 6.6,
        "axes.linewidth": 0.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)

CMAP = LinearSegmentedColormap.from_list(
    "tls_yellow_red",
    ["#EEF4E7", "#F8E7A3", "#F4B45E", "#E66D61", "#C9365E"],
)


def px2pt(box_px: tuple[float, float, float, float]) -> fitz.Rect:
    """Coordinates were read from a 2x-rendered source PDF preview."""
    x0, y0, x1, y1 = box_px
    return fitz.Rect(x0 / 2, y0 / 2, x1 / 2, y1 / 2)


def render_clip(page: fitz.Page, box_px: tuple[float, float, float, float], zoom: float = 5.5) -> np.ndarray:
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=px2pt(box_px), alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if arr.shape[2] > 3:
        arr = arr[:, :, :3]
    return arr


def show_crop(ax, image: np.ndarray, title: str):
    ax.imshow(image)
    ax.set_title(title, fontsize=6.7, fontweight="bold", pad=2.4)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.45)
        spine.set_color("#3A3A3A")


def add_panel_label(fig: plt.Figure, ax: plt.Axes, label: str):
    box = ax.get_position()
    fig.text(box.x0 - 0.015, box.y1 + 0.004, label, fontsize=9, fontweight="bold", ha="right", va="bottom")


def add_colorbar_axis(fig: plt.Figure, ax: plt.Axes, label: str, ticks: list[int]):
    box = ax.get_position()
    cax = fig.add_axes([box.x1 + 0.008, box.y0 + 0.16 * box.height, 0.011, 0.62 * box.height])
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    cax.imshow(grad, aspect="auto", cmap=CMAP, origin="lower")
    cax.set_xticks([])
    tick_pos = np.linspace(0, 255, len(ticks))
    cax.set_yticks(tick_pos)
    cax.set_yticklabels([str(t) for t in ticks], fontsize=5.8)
    cax.yaxis.tick_right()
    cax.tick_params(length=1.6, width=0.45)
    cax.set_title(label, fontsize=6.1, fontweight="bold", pad=2)
    for spine in cax.spines.values():
        spine.set_visible(False)


def save_pub(fig: plt.Figure, stem: str):
    fig.savefig(OUT / f"{stem}.pdf", facecolor="white")
    fig.savefig(OUT / f"{stem}.svg", facecolor="white")
    fig.savefig(OUT / f"{stem}.png", dpi=600, facecolor="white")
    fig.savefig(OUT / f"{stem}.tiff", dpi=600, facecolor="white")
    plt.close(fig)


def main():
    doc = fitz.open(SRC_PDF)
    page = doc[0]

    # Clip boxes in the coordinate system of a 2x-rendered preview.
    a_boxes = [
        (47, 38, 212, 151),
        (218, 38, 380, 151),
        (386, 38, 548, 151),
        (553, 38, 715, 151),
        (721, 38, 889, 151),
    ]
    b_boxes = [
        (47, 172, 255, 313),
        (262, 172, 469, 313),
        (475, 172, 682, 313),
        (687, 172, 895, 313),
    ]
    c_boxes = [
        (49, 344, 387, 579),
        (547, 344, 887, 579),
    ]
    d_boxes = [
        (49, 604, 329, 795),
        (333, 604, 611, 795),
        (615, 604, 895, 795),
        (49, 829, 329, 998),
        (333, 829, 611, 998),
        (615, 829, 895, 998),
    ]

    a_imgs = [render_clip(page, b) for b in a_boxes]
    b_imgs = [render_clip(page, b) for b in b_boxes]
    c_imgs = [render_clip(page, b) for b in c_boxes]
    d_imgs = [render_clip(page, b) for b in d_boxes]

    fig = plt.figure(figsize=(180 / 25.4, 188 / 25.4), facecolor="white")
    gs = fig.add_gridspec(4, 1, height_ratios=[0.86, 1.04, 1.42, 2.15], hspace=0.32)

    gs_a = gs[0].subgridspec(1, 5, wspace=0.055)
    ax_a = [fig.add_subplot(gs_a[0, i]) for i in range(5)]
    for ax, img, title in zip(
        ax_a,
        a_imgs,
        ["TLS integrated", "mregDC/TLS axis", "mregDC extended", "AP/MHC proxy", "IF-core proxy"],
    ):
        show_crop(ax, img, title)

    gs_b = gs[1].subgridspec(1, 4, wspace=0.065)
    ax_b = [fig.add_subplot(gs_b[0, i]) for i in range(4)]
    for ax, img, title in zip(ax_b, b_imgs, ["MYH11", "EEF1G", "H19", "LAPTM4B"]):
        show_crop(ax, img, title)

    gs_c = gs[2].subgridspec(1, 2, wspace=0.16)
    ax_c = [fig.add_subplot(gs_c[0, i]) for i in range(2)]
    for ax, img, title in zip(ax_c, c_imgs, ["TLS score map", "TLS/mregDC co-high cells"]):
        show_crop(ax, img, title)

    gs_d = gs[3].subgridspec(2, 3, wspace=0.055, hspace=0.22)
    ax_d = [fig.add_subplot(gs_d[i, j]) for i in range(2) for j in range(3)]
    for ax, img, title in zip(ax_d, d_imgs, ["MYH11", "CNN1", "C11orf96", "C7", "NAMPT", "SOX2-OT"]):
        show_crop(ax, img, title)

    fig.subplots_adjust(left=0.04, right=0.89, top=0.985, bottom=0.02)
    add_panel_label(fig, ax_a[0], "A")
    add_colorbar_axis(fig, ax_a[-1], "score", [0, 2, 4, 6, 8])
    add_panel_label(fig, ax_b[0], "B")
    add_colorbar_axis(fig, ax_b[-1], "log1p", [0, 1, 2, 3, 4])
    add_panel_label(fig, ax_c[0], "C")
    add_colorbar_axis(fig, ax_c[-1], "TLS", [0, 2, 4, 6, 8])
    add_panel_label(fig, ax_d[0], "D")
    add_colorbar_axis(fig, ax_d[2], "log1p", [0, 1, 2, 3, 4])
    save_pub(fig, "FigureS3_Xenium_spatial_maps_redraw")


if __name__ == "__main__":
    main()
