from __future__ import annotations

from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image


ROOT = Path("/mnt/e/Reserch/MregDC/JTM_SpringerNature_submission_20260602")
SRC = ROOT / "figures"
OUT = ROOT / "figures_for_upload_compressed"


def compress_pdf_to_jpeg_pdf(src: Path, dst: Path, dpi: int = 300, quality: int = 92) -> None:
    doc = fitz.open(src)
    if doc.page_count != 1:
        raise ValueError(f"{src.name} has {doc.page_count} pages; expected one page")
    page = doc[0]
    zoom = dpi / 72
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    jpeg = BytesIO()
    img.save(jpeg, format="JPEG", quality=quality, optimize=True, progressive=True)
    jpeg_bytes = jpeg.getvalue()

    out_doc = fitz.open()
    rect = page.rect
    out_page = out_doc.new_page(width=rect.width, height=rect.height)
    out_page.insert_image(rect, stream=jpeg_bytes)
    out_doc.save(dst, garbage=4, deflate=True)
    out_doc.close()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    report = []
    for src in sorted(SRC.glob("Fig*.pdf")):
        dst = OUT / src.name
        compress_pdf_to_jpeg_pdf(src, dst)
        report.append(
            f"{src.name}\t{src.stat().st_size / 1024 / 1024:.2f}\t{dst.stat().st_size / 1024 / 1024:.2f}"
        )
    (OUT / "compressed_figure_size_report.tsv").write_text(
        "figure\toriginal_MB\tcompressed_MB\n" + "\n".join(report) + "\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()
