# %% markdown
# # extract personal traits, put into a csv file
# 1. [ ] AI literacy
# 2. [ ] DoC
# 3. [ ] IPQ
# 4. [ ] SUS

# %% 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

import HZutil

# %%
to_combine = [folder for folder in os.listdir('data_intermediate') if folder.startswith('P')]

df_ai_all = pd.DataFrame()
df_doc_all = pd.DataFrame()

ai_list, doc_list = [], []
for pp in to_combine:
    df = pd.read_csv(f'data_intermediate/{pp}/resQues_post_{pp}.csv')
    df["answer_num"] = df["answer"].astype(str).str.extract(r"^(\d+)").astype(float)

    df_ai = df[df['section']=='2-2']
    ai_list.append(df_ai.groupby(["pp","index"])["answer_num"].mean()
                          .groupby("pp").mean().reset_index())

    df_doc = df[df['section']=='2-3']
    doc_list.append(df_doc.groupby(["pp","index"])["answer_num"].mean()
                           .groupby("pp").mean().reset_index())

df_ai_all = pd.concat(ai_list, ignore_index=True)
df_doc_all = pd.concat(doc_list, ignore_index=True)

df_doc_all.rename(columns={"answer_num": "DoC"}, inplace=True)
df_doc_all['DoC_z'] = df_doc_all['DoC'].transform(lambda x: (x - x.mean()) / x.std())

df_traits = pd.merge(df_ai_all, df_doc_all, on='pp', how='outer')
df_traits.to_csv('data_analysis/pp_traits.csv', index=False)

# %%
df_traits = pd.read_csv('data_analysis/pp_traits.csv')
wide = pd.read_csv('data_analysis/trial_wise_SoA_cleaned_wide.csv')
df_score = wide.merge(
    df_traits[["pp", "AI_literacy_z", "DoC_z"]],
    on="pp",
    how="left"
)
df_score.to_csv("data_analysis/trial_wise_SoA_with_pp_traits.csv", index=False)

# %%