from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

try:
    import fitz
except Exception:  # pragma: no cover - reported in output metadata
    fitz = None


ROOT = Path("/mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629")
SRC = ROOT / "07_submission_package_R1" / "latex_source_clean"
OUT = ROOT / "08_supplementary_figure_upgrade_20260702" / "current_previews"
OUT.mkdir(parents=True, exist_ok=True)

FIGURES = {
    "S1_singleCellHaystack": SRC / "FigureS1_singleCellHaystack.png",
    "S2_Hotspot": SRC / "FigureS2_Hotspot.png",
    "S3_Xenium_spatial_maps": SRC / "FigureS3_Xenium_spatial_maps-re.pdf",
    "S4_multi_sample_spatial_validation": SRC / "FigureS4_multi_sample_spatial_validation.png",
    "S5_model_validation": SRC / "FigureS5_model_validation.png",
    "S6_specificity_adjusted": SRC / "FigureS6_specificity_adjusted_associations.png",
    "S7_drug_prioritization": ROOT
    / "07_submission_package_R1"
    / "Supplementary_Figure_S7_drug_prioritization.pdf",
}


def render_pdf_page(path: Path, label: str) -> tuple[dict, Image.Image | None]:
    info: dict = {"label": label, "path": str(path)}
    if fitz is None:
        info["error"] = "pymupdf_missing"
        return info, None
    doc = fitz.open(path)
    page = doc[0]
    info["pages"] = len(doc)
    info["page0_pt"] = [round(page.rect.width, 2), round(page.rect.height, 2)]
    info["page0_mm"] = [
        round(page.rect.width / 72 * 25.4, 2),
        round(page.rect.height / 72 * 25.4, 2),
    ]
    pix = page.get_pixmap(matrix=fitz.Matrix(160 / 72, 160 / 72), alpha=False)
    preview = OUT / f"{label}.png"
    pix.save(preview)
    info["preview_png"] = str(preview)
    image = Image.open(preview).convert("RGB")
    info["preview_px"] = list(image.size)
    doc.close()
    return info, image


def render_image(path: Path, label: str) -> tuple[dict, Image.Image]:
    image = Image.open(path).convert("RGB")
    preview = OUT / f"{label}.png"
    image.save(preview)
    info = {
        "label": label,
        "path": str(path),
        "px": list(image.size),
        "preview_png": str(preview),
    }
    return info, image


def make_contact_sheet(thumbs: list[tuple[str, Image.Image]]) -> Path:
    cell_w, cell_h = 560, 390
    cols = 2
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (label, image) in enumerate(thumbs):
        row, col = divmod(i, cols)
        max_w, max_h = cell_w - 30, cell_h - 60
        thumb = image.copy()
        thumb.thumbnail((max_w, max_h), Image.LANCZOS)
        x = col * cell_w + (cell_w - thumb.width) // 2
        y = row * cell_h + 45 + (max_h - thumb.height) // 2
        sheet.paste(thumb, (x, y))
        draw.text((col * cell_w + 15, row * cell_h + 12), label, fill=(20, 20, 20))
        draw.rectangle(
            [col * cell_w + 5, row * cell_h + 5, (col + 1) * cell_w - 6, (row + 1) * cell_h - 6],
            outline=(220, 220, 220),
            width=1,
        )
    out_path = OUT / "current_supplementary_contact_sheet.png"
    sheet.save(out_path)
    return out_path


def main() -> None:
    meta = []
    thumbs = []
    for label, path in FIGURES.items():
        base = {
            "label": label,
            "path": str(path),
            "exists": path.exists(),
            "bytes": path.stat().st_size if path.exists() else None,
        }
        if not path.exists():
            meta.append(base)
            continue
        if path.suffix.lower() == ".pdf":
            info, image = render_pdf_page(path, label)
        else:
            info, image = render_image(path, label)
        info.update(base)
        meta.append(info)
        if image is not None:
            thumbs.append((label, image))

    sheet = make_contact_sheet(thumbs)
    (OUT / "current_supplementary_inventory.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    lines = ["# Current Supplementary Figure Inventory", ""]
    for item in meta:
        lines.append(
            "- {label}: exists={exists}, bytes={bytes}, px={px}, pages={pages}, "
            "page0_mm={page0_mm}, preview={preview}".format(
                label=item.get("label"),
                exists=item.get("exists"),
                bytes=item.get("bytes"),
                px=item.get("px"),
                pages=item.get("pages"),
                page0_mm=item.get("page0_mm"),
                preview=item.get("preview_png"),
            )
        )
    (OUT / "current_supplementary_inventory.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(sheet)


if __name__ == "__main__":
    main()
