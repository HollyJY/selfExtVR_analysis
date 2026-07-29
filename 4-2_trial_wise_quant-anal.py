# %% [markdown]
# # trial wise responses analysis

# * [x] LMM: linear mixed effects model
# * [-] pairwise comparison => R
# * [x] check the distribution of the residual of LMM
# * [ ] acceptance: cumulative link mixture models

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats

import HZutil

# %%
li_resp_LMM = ['SoPA', 'SoNA', 'SoA']
li_resp_CLMM = ['Accept']

# %% read file
long = pd.read_csv('data_analysis/trial_wise_SoA_cleaned_long.csv')
wide = pd.read_csv('data_analysis/trial_wise_SoA_cleaned_wide.csv')

# %% check distribution of the responses
# not necessary!!!! because should check after fitting LLM, residuals
g = sns.catplot(
    data=long,
    x="condition",
    y="rate",
    hue="voice_id",
    col="response_type",
    kind="strip",
    jitter=True,
    sharey=False
)
g.figure.suptitle("Responses")
g.figure.set_size_inches(12, 4)
g.tight_layout()
g.savefig('fig/response_distribution.png', dpi=1000)

# 1. histplot
g = sns.FacetGrid(long, col="response_type", margin_titles=True)
g.map(sns.histplot, "rate", kde=True, fill = True)
g.figure.suptitle("Distribution of responses")
g.figure.set_size_inches(12, 4)
g.tight_layout()
g.savefig('fig/response_distribution.png', dpi=1000)

# q-q plot
plt.subplots(1, 4, figsize=(12, 3))
for i in range(4):
    plt.subplot(1, 4, i+1)
    stats.probplot(wide.iloc[:, i+4].dropna(), dist="norm", plot=plt)
    plt.title(wide.columns[i+4])
plt.suptitle("Q-Q plot of responses")
plt.tight_layout()
plt.savefig('fig/response_qqplot.png', dpi=1000)
plt.show()

# # Shapiro-Wilk test
# from scipy.stats import shapiro

# for col in wide.columns[4:]:
#     stat, p = shapiro(wide[col].dropna())
#     print(f"{col}: stat={stat:.4f}, p={p:.4f}")

# TODO: repeated-measures agency => check normality of residuals? 

# %%
# # linear mixed effects model
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm

def plot_mixedlm_diagnostics(mdf, title=""):
    resid = mdf.resid
    fitted = mdf.fittedvalues

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    sns.histplot(resid, kde=True, ax=axes[0])
    axes[0].set_title(f"{title} residual distribution")
    axes[0].set_xlabel("Residuals")

    sm.qqplot(resid, line="45", ax=axes[1])
    axes[1].set_title(f"{title} Q-Q plot")

    sns.scatterplot(x=fitted, y=resid, ax=axes[2], color='blue', alpha=0.5)
    axes[2].axhline(0, linestyle="--", linewidth=1)
    axes[2].set_title(f"{title} residuals vs fitted")
    axes[2].set_xlabel("Fitted values")
    axes[2].set_ylabel("Residuals")

    plt.tight_layout()
    plt.show()

def random_effects_variance(mdf):
    pp_var = mdf.cov_re.iloc[0, 0] if mdf.cov_re.shape[0] > 0 else 0
    trial_var = mdf.vcomp[0] if len(mdf.vcomp) > 0 else 0
    resid_var = mdf.scale
    total_var = pp_var + trial_var + resid_var
    print("Random effects variance:")
    print("pp_var: {}, trial_var: {}, resid_var: {}, total_var: {}".format(pp_var, trial_var, resid_var, total_var))
    print("pp proportion: {}, trial proportion: {}, resid proportion: {}".format(pp_var / total_var, trial_var / total_var, resid_var / total_var))
    return

# %% main model
# rate ~ condition * voice_id + (1 | pp)
display(wide.head(3))

for resp in li_resp_LMM:
    md = mixedlm(
        f"{resp} ~ C(condition) * C(voice_id)",
        data=wide,
        groups=wide["pp"],
    )
    mdf = md.fit()
    print(mdf.summary())
    # random effect variance
    random_effects_variance(mdf)
    # check model diagnostics, redisuals
    plot_mixedlm_diagnostics(mdf, title=f"{resp} LMM diagnosis")


# %% participant-level covariates
# rate ~ condition * voice_id + AI_literacy_z + DoC_z + (1 | pp)
# covariates: AI literacy, DoC, fixed effects
# random effects / intercepts: pp, scene_id

df_traits = pd.read_csv('data_analysis/pp_traits.csv')
df_score = wide.merge(
    df_traits[["pp", "AI_literacy_z", "DoC_z"]],
    on="pp",
    how="left"
)

for resp in li_resp_LMM:
    md = mixedlm(
        f"{resp} ~ C(condition) * C(voice_id) + AI_literacy_z + DoC_z",
        data=df_score,
        groups=df_score["pp"],
        re_formula="1",
    )
    mdf = md.fit()
    print(mdf.summary())
    # random effect variance
    random_effects_variance(mdf)
    # check model diagnostics, redisuals
    plot_mixedlm_diagnostics(mdf, title=f"{resp} LMM diagnosis")

# %%
display(wide.head(3))
# %%
