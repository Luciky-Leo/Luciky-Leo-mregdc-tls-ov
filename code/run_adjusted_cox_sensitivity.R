root <- "/mnt/e/Reserch/MregDC/JTM_SpringerNature_submission_20260602"
source_dir <- file.path(root, "source_data", "Fig09_LASSO_Cox_internal_validation")

infile <- file.path(source_dir, "source_model_input_patients_with_gdc_clinical.csv")
outfile <- file.path(source_dir, "Source_Data_Survival_adjusted_Cox_sensitivity.csv")
coverage_out <- file.path(source_dir, "Source_Data_Survival_adjusted_Cox_covariate_coverage.csv")

if (!requireNamespace("survival", quietly = TRUE)) stop("Missing R package: survival")

dat <- utils::read.csv(infile, stringsAsFactors = FALSE, check.names = FALSE)
dat <- dat[is.finite(dat$OS_time) & is.finite(dat$OS_event) & is.finite(dat$risk_score) & dat$OS_time > 0, ]

clean_text <- function(x) {
  x <- trimws(as.character(x))
  x[x == "" | tolower(x) %in% c("not reported", "not applicable", "unknown", "nan", "na")] <- NA
  x
}

dat$age_years <- suppressWarnings(as.numeric(dat$age_at_index_years))
if (sum(is.finite(dat$age_years)) < 50) {
  dat$age_years <- suppressWarnings(as.numeric(dat$age_at_diagnosis_years))
}

dat$figo_stage_clean <- clean_text(dat$figo_stage)
dat$tumor_stage_clean <- clean_text(dat$tumor_stage)
dat$stage_clean <- ifelse(!is.na(dat$figo_stage_clean), dat$figo_stage_clean, dat$tumor_stage_clean)
dat$stage_clean <- gsub("Stage ", "", dat$stage_clean, fixed = TRUE)
dat$stage_clean <- gsub("stage ", "", dat$stage_clean, fixed = TRUE)
dat$stage_clean <- gsub("[ABC]$", "", dat$stage_clean)
dat$stage_clean[grepl("^I$", dat$stage_clean, ignore.case = TRUE)] <- "I"
dat$stage_clean[grepl("^II$", dat$stage_clean, ignore.case = TRUE)] <- "II"
dat$stage_clean[grepl("^III", dat$stage_clean, ignore.case = TRUE)] <- "III"
dat$stage_clean[grepl("^IV", dat$stage_clean, ignore.case = TRUE)] <- "IV"
dat$stage_clean <- factor(dat$stage_clean)

dat$grade_clean <- clean_text(dat$tumor_grade)
dat$grade_clean <- factor(dat$grade_clean)
dat$residual_disease_clean <- factor(clean_text(dat$residual_disease))
dat$advanced_stage_III_IV <- ifelse(as.character(dat$stage_clean) %in% c("III", "IV"), 1,
  ifelse(as.character(dat$stage_clean) %in% c("I", "II"), 0, NA))
dat$high_grade_G3_G4_GB <- ifelse(as.character(dat$grade_clean) %in% c("G3", "G4", "GB"), 1,
  ifelse(as.character(dat$grade_clean) %in% c("G1", "G2"), 0, NA))

candidate_covariates <- c(
  "age_years",
  "stage_clean",
  "advanced_stage_III_IV",
  "grade_clean",
  "high_grade_G3_G4_GB",
  "residual_disease_clean"
)
coverage <- do.call(rbind, lapply(candidate_covariates, function(col) {
  x <- dat[[col]]
  non_missing <- if (is.factor(x)) !is.na(x) else is.finite(x)
  data.frame(
    covariate = col,
    non_missing_n = sum(non_missing),
    model_patients_n = nrow(dat),
    non_missing_fraction = mean(non_missing),
    unique_non_missing_values = paste(unique(as.character(x[non_missing]))[1:min(12, length(unique(as.character(x[non_missing]))))], collapse = "; "),
    stringsAsFactors = FALSE
  )
}))
utils::write.csv(coverage, coverage_out, row.names = FALSE)

# Use collapsed clinical terms for the main sensitivity model to avoid sparse
# categorical levels that produce separation-like Cox estimates in TCGA-OV.
usable_covariates <- c("age_years", "advanced_stage_III_IV", "high_grade_G3_G4_GB")
usable_covariates <- usable_covariates[vapply(usable_covariates, function(col) {
  x <- dat[[col]]
  non_missing <- is.finite(x)
  sum(non_missing) >= 100 && length(unique(x[non_missing])) >= 2
}, logical(1))]

fit_model <- function(name, vars) {
  need <- c("OS_time", "OS_event", vars)
  d <- dat[, need, drop = FALSE]
  keep <- stats::complete.cases(d)
  d <- d[keep, , drop = FALSE]
  if (nrow(d) < 100) return(NULL)
  form <- stats::as.formula(paste("survival::Surv(OS_time, OS_event) ~", paste(vars, collapse = " + ")))
  fit <- survival::coxph(form, data = d)
  sm <- summary(fit)
  out <- data.frame(
    model = name,
    n = nrow(d),
    events = sum(d$OS_event),
    term = rownames(sm$coefficients),
    HR = sm$coefficients[, "exp(coef)"],
    lower95 = sm$conf.int[, "lower .95"],
    upper95 = sm$conf.int[, "upper .95"],
    p = sm$coefficients[, "Pr(>|z|)"],
    stringsAsFactors = FALSE
  )
  out
}

models <- list()
models[[1]] <- fit_model("risk_score_only", c("risk_score"))
if (length(usable_covariates) > 0) {
  models[[2]] <- fit_model("risk_score_plus_age_stage_grade_sensitivity", c("risk_score", usable_covariates))
}
res <- do.call(rbind, models[!vapply(models, is.null, logical(1))])
res$p_adj_BH_within_table <- stats::p.adjust(res$p, method = "BH")
utils::write.csv(res, outfile, row.names = FALSE)

message("Usable covariates: ", paste(usable_covariates, collapse = ", "))
message("Wrote ", outfile)
message("Wrote ", coverage_out)
