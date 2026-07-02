suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(cowplot)
  library(patchwork)
  library(ggrepel)
  library(ragg)
})

project_root <- "/mnt/e/Reserch/MregDC_Cancers_R1_Revision_20260629"
source_csv <- file.path(
  project_root,
  "07_submission_package_R1/_source_data_stage/FigS07_drug_prioritization_docking/FigS07_CH_drug_vulnerability_matrix_source_matrix.csv"
)
out_dir <- file.path(project_root, "08_supplementary_figure_upgrade_20260702/outputs")
table_dir <- file.path(project_root, "08_supplementary_figure_upgrade_20260702/intermediate_tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)

raw <- read.csv(source_csv, check.names = FALSE)
stopifnot("feature" %in% names(raw))

class_map <- tibble::tribble(
  ~feature, ~target_class,
  "Baricitinib", "JAK inhibitor",
  "Ruxolitinib", "JAK inhibitor",
  "Fedratinib", "JAK inhibitor",
  "Tofacitinib", "JAK inhibitor",
  "Napabucasin", "STAT3-axis",
  "Stattic", "STAT3-axis",
  "Bortezomib", "Proteasome",
  "Carfilzomib", "Proteasome",
  "Ixazomib", "Proteasome",
  "BMS-345541", "IKK/NF-kB",
  "TPCA-1", "IKK/NF-kB",
  "Curcumin", "Polyphenol"
)

evidence_cols <- c(
  "clinical", "target direct", "virtual screen", "risk reversal",
  "TLS suppression", "axis suppression", "IF suppression",
  "AP suppression", "docking"
)
stopifnot(all(evidence_cols %in% names(raw)))

label_map <- c(
  "clinical" = "Clinical",
  "target direct" = "Target",
  "virtual screen" = "Virtual",
  "risk reversal" = "Risk",
  "TLS suppression" = "TLS",
  "axis suppression" = "Axis",
  "IF suppression" = "IF",
  "AP suppression" = "AP",
  "docking" = "Docking"
)

class_order <- c("JAK inhibitor", "STAT3-axis", "Proteasome", "IKK/NF-kB", "Polyphenol")
class_cols <- c(
  "JAK inhibitor" = "#D63C79",
  "STAT3-axis" = "#7A5195",
  "Proteasome" = "#3B73B9",
  "IKK/NF-kB" = "#E6A532",
  "Polyphenol" = "#42A66A"
)

dat <- raw %>%
  left_join(class_map, by = "feature") %>%
  mutate(
    target_class = factor(target_class, levels = class_order),
    mean_priority = rowMeans(across(all_of(evidence_cols)), na.rm = TRUE),
    target_evidence = rowMeans(across(c("clinical", "target direct", "virtual screen")), na.rm = TRUE),
    program_reversal = rowMeans(across(c("risk reversal", "TLS suppression", "axis suppression", "IF suppression", "AP suppression")), na.rm = TRUE),
    docking_support = .data[["docking"]]
  ) %>%
  arrange(target_class, desc(mean_priority)) %>%
  mutate(
    compound = factor(feature, levels = rev(feature)),
    row_id = row_number()
  )

derived <- dat %>%
  select(
    compound = feature, target_class, mean_priority, target_evidence,
    program_reversal, docking_support, all_of(evidence_cols)
  )
write.table(
  derived,
  file.path(table_dir, "FigS7_drug_prioritization_derived_scores.tsv"),
  sep = "\t", quote = FALSE, row.names = FALSE
)

heat_long <- dat %>%
  select(feature, compound, target_class, all_of(evidence_cols)) %>%
  pivot_longer(all_of(evidence_cols), names_to = "layer", values_to = "z") %>%
  mutate(layer_label = factor(label_map[layer], levels = unname(label_map[evidence_cols])))

base_family <- "sans"
theme_panel <- function(base_size = 7) {
  theme_classic(base_size = base_size, base_family = base_family) +
    theme(
      plot.title = element_text(face = "bold", size = base_size + 1, hjust = 0, margin = margin(b = 3)),
      axis.title = element_text(size = base_size),
      axis.text = element_text(size = base_size, color = "#202833"),
      axis.line = element_line(linewidth = 0.28, color = "#202833"),
      axis.ticks = element_line(linewidth = 0.25, color = "#202833"),
      legend.title = element_text(size = base_size, face = "bold"),
      legend.text = element_text(size = base_size - 0.5),
      legend.key.height = unit(3.5, "mm"),
      legend.key.width = unit(3.5, "mm"),
      plot.margin = margin(3, 3, 3, 3)
    )
}

strip_df <- dat %>%
  transmute(compound, target_class)

p_strip <- ggplot(strip_df, aes(x = 1, y = compound, fill = target_class)) +
  geom_tile(width = 0.92, height = 0.92) +
  scale_fill_manual(values = class_cols, drop = FALSE) +
  scale_y_discrete(drop = FALSE) +
  labs(x = NULL, y = NULL) +
  theme_void(base_family = base_family) +
  theme(legend.position = "none", plot.margin = margin(17, 1, 19, 1))

p_heat <- ggplot(heat_long, aes(x = layer_label, y = compound, fill = z)) +
  geom_tile(width = 0.94, height = 0.94, color = "white", linewidth = 0.25) +
  scale_fill_gradient2(
    low = "#6E83B7", mid = "#F7F7F7", high = "#F36F63",
    midpoint = 0, limits = c(-2.1, 2.1), oob = scales::squish,
    name = "z"
  ) +
  scale_x_discrete(expand = expansion(mult = c(0.01, 0.01))) +
  scale_y_discrete(drop = FALSE, expand = expansion(mult = c(0.01, 0.01))) +
  labs(title = "Evidence matrix", x = NULL, y = NULL) +
  guides(fill = guide_colorbar(frame.colour = "#202833", ticks.colour = "white", barheight = unit(23, "mm"))) +
  theme_panel(7) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1, face = "bold"),
    axis.text.y = element_text(face = "bold"),
    axis.line = element_blank(),
    axis.ticks = element_blank(),
    legend.position = "right",
    plot.margin = margin(4, 3, 4, 12)
  )

p_a <- p_heat

rank_df <- dat %>%
  arrange(mean_priority) %>%
  mutate(compound_rank = factor(feature, levels = feature))

p_b <- ggplot(rank_df, aes(x = mean_priority, y = compound_rank, fill = target_class)) +
  geom_vline(xintercept = 0, linewidth = 0.25, linetype = "dashed", color = "#6B7280") +
  geom_col(width = 0.66, color = "white", linewidth = 0.25) +
  scale_fill_manual(values = class_cols, drop = FALSE, name = "class") +
  labs(title = "Integrated priority", x = "mean z across layers", y = NULL) +
  theme_panel(7) +
  guides(fill = guide_legend(override.aes = list(size = 4), title = "class")) +
  theme(legend.position = "right", axis.text.y = element_text(face = "bold"))

label_set <- c("Baricitinib", "Ruxolitinib", "Carfilzomib", "Curcumin", "Fedratinib")
p_c <- ggplot(dat, aes(x = mean_priority, y = docking_support, color = target_class)) +
  geom_hline(yintercept = 0, linewidth = 0.25, linetype = "dashed", color = "#6B7280") +
  geom_vline(xintercept = 0, linewidth = 0.25, linetype = "dashed", color = "#6B7280") +
  geom_point(size = 2.8, alpha = 0.92, stroke = 0.25) +
  ggrepel::geom_text_repel(
    data = dat %>% filter(feature %in% label_set),
    aes(label = feature),
    family = base_family, size = 2.2, min.segment.length = 0,
    segment.size = 0.25, box.padding = 0.18, point.padding = 0.15,
    max.overlaps = Inf, seed = 7
  ) +
  scale_color_manual(values = class_cols, drop = FALSE, name = "class") +
  labs(title = "Docking support vs priority", x = "integrated priority", y = "docking z") +
  theme_panel(7) +
  guides(color = "none") +
  theme(legend.position = "none")

class_profile <- dat %>%
  group_by(target_class) %>%
  summarise(
    `Target evidence` = mean(target_evidence, na.rm = TRUE),
    `Program reversal` = mean(program_reversal, na.rm = TRUE),
    `Docking` = mean(docking_support, na.rm = TRUE),
    n = dplyr::n(),
    .groups = "drop"
  ) %>%
  mutate(target_class = factor(target_class, levels = class_order)) %>%
  pivot_longer(c(`Target evidence`, `Program reversal`, `Docking`), names_to = "summary_layer", values_to = "z") %>%
  mutate(
    target_class = factor(as.character(target_class), levels = rev(class_order)),
    summary_layer = factor(summary_layer, levels = c("Target evidence", "Program reversal", "Docking"))
  )

p_d <- ggplot(class_profile, aes(x = summary_layer, y = target_class, fill = z)) +
  geom_tile(width = 0.93, height = 0.82, color = "white", linewidth = 0.3) +
  scale_fill_gradient2(
    low = "#6E83B7", mid = "#F7F7F7", high = "#F36F63",
    midpoint = 0, limits = c(-1.5, 1.5), oob = scales::squish,
    name = "mean z"
  ) +
  scale_x_discrete(expand = expansion(mult = c(0.02, 0.02))) +
  labs(title = "Target-class summary", x = NULL, y = NULL) +
  theme_panel(7) +
  guides(fill = "none") +
  theme(
    axis.text.x = element_text(angle = 30, hjust = 1, vjust = 1, face = "bold"),
    axis.text.y = element_text(face = "bold"),
    axis.line = element_blank(),
    axis.ticks = element_blank(),
    legend.position = "none"
  )

final_plot <- cowplot::plot_grid(
  p_a, p_b, p_c, p_d,
  labels = c("A", "B", "C", "D"),
  label_fontfamily = base_family,
  label_fontface = "bold",
  label_size = 10,
  label_x = c(0.006, 0.006, 0.006, 0.006),
  label_y = c(0.995, 0.995, 0.995, 0.995),
  ncol = 2,
  rel_widths = c(1.55, 1.05),
  rel_heights = c(1.25, 1.0),
  align = "hv",
  axis = "tblr"
)

width_in <- 180 / 25.4
height_in <- 145 / 25.4

pdf_out <- file.path(out_dir, "Supplementary_Figure_S7_drug_prioritization_redraw.pdf")
svg_out <- file.path(out_dir, "Supplementary_Figure_S7_drug_prioritization_redraw.svg")
png_out <- file.path(out_dir, "Supplementary_Figure_S7_drug_prioritization_redraw.png")
tiff_out <- file.path(out_dir, "Supplementary_Figure_S7_drug_prioritization_redraw.tiff")

ggsave(pdf_out, final_plot, width = width_in, height = height_in, device = cairo_pdf, bg = "white")
grDevices::svg(svg_out, width = width_in, height = height_in, bg = "white", onefile = FALSE)
print(final_plot)
dev.off()
ragg::agg_png(png_out, width = width_in, height = height_in, units = "in", res = 600, background = "white")
print(final_plot)
dev.off()
ragg::agg_tiff(tiff_out, width = width_in, height = height_in, units = "in", res = 600, background = "white", compression = "lzw")
print(final_plot)
dev.off()

message("Wrote: ", pdf_out)
message("Wrote: ", svg_out)
message("Wrote: ", png_out)
message("Wrote: ", tiff_out)
message("Wrote derived table: ", file.path(table_dir, "FigS7_drug_prioritization_derived_scores.tsv"))
