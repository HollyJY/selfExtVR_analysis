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

for pp in to_combine:
    # ai_literacy
    df = pd.read_csv(f'data_intermediate/{pp}/resQues_post_{pp}.csv')

    # AI literacy
    df_ai = df[df['section']=='2-2']
    df_ai["answer_num"] = (
        df_ai["answer"]
        .astype(str)
        .str.extract(r"^(\d+)")
        .astype(float)
    )
    df_ai = df_ai.pivot_table(
        index=["pp", "index"],
        values="answer_num",
        aggfunc="mean"
    ).reset_index()
    df_ai_all = pd.concat([df_ai_all, df_ai.groupby("pp")["answer_num"].mean().reset_index()], ignore_index=True)

    # DoC
    df_doc = df[df['section']=='2-3']
    df_doc["answer_num"] = (
        df_doc["answer"]
        .astype(str)
        .str.extract(r"^(\d+)")
        .astype(float)
    )
    df_doc = df_doc.pivot_table(
        index=["pp", "index"],
        values="answer_num",
        aggfunc="mean"
    ).reset_index()
    df_doc_all = pd.concat([df_doc_all, df_doc.groupby("pp")["answer_num"].mean().reset_index()], ignore_index=True)

df_ai_all.rename(columns={"answer_num": "AI_literacy"}, inplace=True)
df_ai_all['AI_literacy_z'] = df_ai_all['AI_literacy'].transform(lambda x: (x - x.mean()) / x.std())

df_doc_all.rename(columns={"answer_num": "DoC"}, inplace=True)
df_doc_all['DoC_z'] = df_doc_all['DoC'].transform(lambda x: (x - x.mean()) / x.std())

df_traits = pd.merge(df_ai_all, df_doc_all, on='pp', how='outer')
df_traits.to_csv('data_analysis/pp_traits.csv', index=False)
# %%
