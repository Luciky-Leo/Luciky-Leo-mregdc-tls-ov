from __future__ import annotations

from pathlib import Path

import fitz


ROOT = Path("/mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629")
PDF = ROOT / "07_submission_package_R1" / "Supplementary_Information.pdf"
OUT = ROOT / "08_supplementary_figure_upgrade_20260702" / "current_previews"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    doc = fitz.open(PDF)
    pages = []
    for index, page in enumerate(doc, start=1):
        pages.append(f"\n--- PAGE {index} ---\n{page.get_text()}")
    out_path = OUT / "Supplementary_Information_text.txt"
    out_path.write_text("\n".join(pages), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
