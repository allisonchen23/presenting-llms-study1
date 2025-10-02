#!/usr/bin/env Rscript

# List of required packages for this study
required_pkgs <- c(
  "lme4",
  "lmerTest",
  "emmeans",
  "ggplot2",
  "dplyr",
  "tidyr",
  "stringr",
  "psych",
  "car",
  "MuMIn",
  "simr"
)

# Matching conda package names (all lowercase, prefixed with r-)
conda_pkgs <- c(
  "r-base=4.3.1",
  "r-lme4",
  "r-lmertest",
  "r-emmeans",
  "r-ggplot2",
  "r-dplyr",
  "r-tidyr",
  "r-stringr",
  "r-psych",
  "r-car",
  "r-mumin",
  "r-simr"
)

check_and_install <- function(pkgs, conda_pkgs) {
  missing <- character(0)
  for (pkg in pkgs) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      message(sprintf("Package '%s' not found.", pkg))
      missing <- c(missing, pkg)
    } else {
      message(sprintf("Package '%s' is already installed.", pkg))
    }
  }
  
  if (length(missing) > 0) {
    message("\n Installing missing packages with conda...")
    # Always install full list (ensures consistency)
    cmd <- paste(
      "conda install -y -c conda-forge",
      paste(conda_pkgs, collapse = " ")
    )
    message("Running: ", cmd)
    status <- system(cmd)
    if (status != 0) {
      stop("Conda installation failed. See output above.")
    }
  }
}

# Run the check
check_and_install(required_pkgs, conda_pkgs)

cat("\nPackage check complete.\n")
