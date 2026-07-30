## -----------------------------------------------------------------------------
library(tidyverse)   # read_csv, dplyr, ggplot2, etc.
library(lme4)        # lmer()
library(lmerTest)    # p-values for LMM
library(emmeans)     # post hoc comparisons
library(effectsize)  # effect sizes
library(performance) # model diagnostics


## -----------------------------------------------------------------------------
# Response variables analysed using LMM
li_resp_LMM <- c("SoA")
# Single ordinal response analysed using CLMM
li_resp_CLMM <- c("Accept", "Authorship")

long <- read_csv(
  "data_analysis/trial_wise_SoA_cleaned_long.csv",
  show_col_types = FALSE
)
wide <- read_csv(
  "data_analysis/trial_wise_SoA_with_pp_traits.csv",
  show_col_types = FALSE
)


## -----------------------------------------------------------------------------
head(wide, 3)


## -----------------------------------------------------------------------------
# fit lmm model for SoA
lmm_SoA <- lmer(
  SoA ~ condition * voice_id + AI_literacy_z + DoC_z + (1 | pp),
  data = wide
)
summary(lmm_SoA)


## -----------------------------------------------------------------------------
# performance check: check residuals
qqnorm(resid(lmm_SoA))
qqline(resid(lmm_SoA))

plot(lmm_SoA)

performance::check_model(lmm_SoA)


## -----------------------------------------------------------------------------
# omnibus test for SoA / hypothesis testing for SoA
anova(lmm_SoA, type = 3)


## -----------------------------------------------------------------------------
# pairwise comparision
emm <- emmeans(lmm_SoA, pairwise ~ condition | voice_id)
pairs(emm, adjust = "holm")
eff_size(
    emm,
    sigma = sigma(lmm_SoA),
    edf = df.residual(lmm_SoA)
)


## -----------------------------------------------------------------------------
# pairwise comparisons for SoA
emm <- emmeans(lmm_SoA, pairwise ~ voice_id | condition)
pairs(emm, adjust = "holm")
eff_size(
    emm,
    sigma = sigma(lmm_SoA),
    edf = df.residual(lmm_SoA)
)


## -----------------------------------------------------------------------------
# effect size for SoA
# partial η² - the proportion of variance explained by a given effect, partialling out other effects from the total non-error variance
eta_squared(lmm_SoA, partial = TRUE)

# marginal R² - the proportion of variance explained by the fixed effects alone
r2(lmm_SoA)

