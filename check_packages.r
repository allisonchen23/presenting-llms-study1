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

check_and_install <- function(pkgs) {
  for (pkg in pkgs) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      message(sprintf("Package '%s' not found. Installing...", pkg))
      install.packages(pkg, repos = "https://cloud.r-project.org")
    } else {
      message(sprintf("Package '%s' is already installed.", pkg))
    }
  }
}

# Run the check
check_and_install(required_pkgs)

print("Package check complete.")