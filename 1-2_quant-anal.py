# %% [markdown]
# # what to do in the script
# trial wise responses: agency + acceptance
# * [x] remove incomplete trials (std = 0 for all questions; llm failure)
#   * [ ] LLM failures
# * [x] calculate SoPA, SoNA, acceptance, SoA
# * [ ] check the distribution of the responses
# * [ ] cumulative link mixture models

# ---
# ### sense of agency
# * SoPA (Sense of Positive Agency) — 5 items
#   * [1,4,5,7,8]
# * SoNA (Sense of Negative Agency) — 6 items
#   * [2,3,6]

# Scoring, for each participant:

# * $\text{SoPA} = \frac{\sum \text{SoPA items}}{5}$

# * $\text{SoNA} = \frac{\sum \text{SoNA items}}{6}$

# * ❓$\text{SoA} = \text{SoPA} - \text{SoNA}$

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats

import HZutil
# %%
# ## read in the data, long table
df = pd.read_csv('data_analysis/trial_wise_responses.csv')
# df['pp'].value_counts()
df.head(3)

# %% => wide table, for checking each trial
wide = df.pivot_table(
    index=["pp", "trial", "voice_id", "condition"],
    columns="question_index",
    values="answer_index",
    aggfunc="mean"
).reset_index()

wide['ans_sd'] = wide[[1, 2, 3, 4, 5, 6, 7, 8]].std(axis=1)

# %%
# outlier detection and removal
# outlier1, std = 0 for all questions, positive / negative
to_remove = wide[wide['ans_sd']==0]
display(to_remove)

to_remove_pairs = to_remove[["pp", "trial"]].drop_duplicates()
df_1 = df.merge(
    to_remove_pairs,
    on=["pp", "trial"],
    how="left",
    indicator=True
)
df = df_1[df_1["_merge"] == "left_only"].drop(columns="_merge")
wide.drop(to_remove_pairs.index, inplace=True)
display(wide['pp'].value_counts()[wide['pp'].value_counts()<12])

df.to_csv('data_analysis/trial_wise_responses_cleaned.csv', index=False)
df_ct = df['pp'].value_counts()
display(df_ct[df_ct < 108])

# TODO: LLM trial wise results => if doing work correctly

# %% 
# calculate SoPA, SoNA, acceptance, SoPA
wide['SoPA'] = wide[[1, 4, 5, 7, 8]].mean(axis=1)
wide['SoNA'] = wide[[2, 3, 6]].mean(axis=1)
wide['Accept'] = wide[[9]]
# FIXME: how to calculate SoA?
wide['SoA'] = wide['SoPA'] - wide['SoNA']
wide.drop(columns=['ans_sd',1,2,3,4,5,6,7,8,9], inplace=True)
display(wide.head(3))
wide.to_csv('data_analysis/trial_wise_SoA_cleaned_wide.csv', index=False)

long = wide.melt(
    id_vars=["pp", "trial", "voice_id", "condition"],
    var_name="response_type",
    value_name="rate"
)
display(long.head(3))
long.to_csv('data_analysis/trial_wise_SoA_cleaned_long.csv', index=False)

# %% check distribution of the responses
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

# Shapiro-Wilk test
from scipy.stats import shapiro

for col in wide.columns[4:]:
    stat, p = shapiro(wide[col].dropna())
    print(f"{col}: stat={stat:.4f}, p={p:.4f}")

# TODO: repeated-measures agency => check normality of residuals? 

# %%
# # linear mixed effects model
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm

# %% main model
# rate ~ condition * voice_id + (1 | pp) + (1 | trial)
# list_resp_LMM = ['SoPA', 'SoNA', 'Accept', 'SoA']
list_resp_LMM = ['SoPA', 'SoNA']

for resp in list_resp_LMM:
    md = mixedlm(
        f"{resp} ~ C(condition) * C(voice_id)",
        data=wide,
        groups=wide["pp"],
        re_formula="1",
        vc_formula={"trial": "0 + C(trial)"}
    )
    mdf = md.fit()
    print(mdf.summary())
    

# %% participant-level covariates
# rate ~ condition * voice_id + AI_literacy_z + DoC_z + (1 | pp) + (1 | trial)

df_traits = pd.read_csv('data_analysis/pp_traits.csv')
df_score = wide.merge(
    df_traits[["pp", "AI_literacy_z", "DoC_z"]],
    on="pp",
    how="left"
)

for resp in list_resp_LMM:
    md = mixedlm(
        f"{resp} ~ C(condition) * C(voice_id) + AI_literacy_z + DoC_z",
        data=df_score,
        groups=df_score["pp"],
        re_formula="1",
        vc_formula={"trial": "0 + C(trial)"}
    )
    mdf = md.fit()
    print(mdf.summary())

# %%
display(wide.head(3))
# %%
