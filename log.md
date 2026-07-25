@2026-07-25 sat
- [ ] CLMM for acceptance
- [ ] LLM model fitting whole process
  - how to test assumption? => residuals ~ norm; fit model => test assumptions
    - Model diagnosis: plot the normality of the residuals and residuals vs prediction.
    ```python
    plot_lm_diagnosis(residual=lm_glob.resid,
                      prediction=lm_glob.predict(df), group=df.classroom)
    ```
  - Model Selection Criteria
    - tests whether adding random effects significantly improves the model.
      - Likelihood Ratio Test: whether adding random effects significantly improves the model
          ```python
          # Compare the fixed and combined models using the likelihood ratio test
          lr_test = combined_model.compare_lr_test(fixed_effects_model)
          print(lr_test)
          ```
      - Akaike Information Criterion (AIC): Penalizes model complexity, with lower values indicating a better model fit.
      - Bayesian Information Criterion (BIC): Similar to AIC, but with a stronger penalty for the number of parameters.
      ```python
      print(f'Fixed Effects Model AIC: {fixed_effects_model.aic}')
      print(f'Random Effects Model AIC: {random_effects_model.aic}')
      print(f'Combined Model AIC: {combined_model.aic}')
      ```

@2026-07-24
- [x] [CLMM](https://metricgate.com/docs/cumulative-link-mixed-model/)
    - Proportional odds assumption: Fixed-effect coefficients are assumed constant across all thresholds, meaning a predictor shifts the entire cumulative probability curve uniformly.
- [x] [LMM](https://duchesnay.github.io/pystatsml/statistics/lmm/lmm.html)
  - [python codes](https://www.statsmodels.org/stable/mixed_linear.html)
  - rate ~ condition * voice_id + AI_literacy_z + DoC_z + (1 | pp) + (1 | trial)
  - (standardized) AI_literacy_z => (AI_literacy - mean(AI_literacy)) / SD(AI_literacy)

@2026-07-23
- [?] *check normality*: the normality of SoNA/SoPA/SoA, or also single questions?
  - for CLMM => no need to check normality??
- [?] *calculate SoA*: average of all scores or average of SoPA,SoNA????

@2026-07-20
- [x] transcribe all the scribes, still on server