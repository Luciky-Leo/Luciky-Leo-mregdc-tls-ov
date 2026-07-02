from pathlib import Path

from PIL import Image, ImageDraw

out = Path("/mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629/08_supplementary_figure_upgrade_20260702/outputs")
files = [
    "FigureS1_singleCellHaystack_redraw.png",
    "FigureS2_Hotspot_redraw.png",
    "FigureS3_Xenium_spatial_maps_redraw.png",
    "FigureS4_multi_sample_spatial_validation_redraw.png",
    "FigureS5_model_validation_redraw.png",
    "FigureS6_specificity_adjusted_associations_redraw.png",
    "Supplementary_Figure_S7_drug_prioritization_redraw.png",
]

thumbs = []
width = 900
pad = 24
label_h = 36
for file_name in files:
    im = Image.open(out / file_name).convert("RGB")
    scale = width / im.width
    im = im.resize((width, int(im.height * scale)))
    canvas = Image.new("RGB", (width, im.height + label_h), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((8, 8), file_name, fill=(20, 30, 45))
    canvas.paste(im, (0, label_h))
    thumbs.append(canvas)

height = sum(t.height for t in thumbs) + pad * (len(thumbs) + 1)
sheet = Image.new("RGB", (width + 2 * pad, height), "white")
y = pad
for thumb in thumbs:
    sheet.paste(thumb, (pad, y))
    y += thumb.height + pad

sheet.save(out / "supplementary_redraw_contact_sheet.png")
