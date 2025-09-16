
source("code/src/mixed_effect_models.R")

power_analysis(
    df_path = "analysis/mental_capacities/factor_analysis/results/R/input_files/factor_analysis.csv",
    n_sim=1000,
    compare_to = c("portray+category", "category"),
    save_dir = "analysis/mental_capacities/factor_analysis/results/R/results",
    save_txt = FALSE,
    show_progress = FALSE,
    overwrite = FALSE
)