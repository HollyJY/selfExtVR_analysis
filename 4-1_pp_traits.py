# %% markdown
# # extract personal traits, put into a csv file
# 1. [x] AI literacy
# 2. [x] DoC
# 3. [ ] IPQ
# 4. [ ] SUS
# 5. [ ] general demographics

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
df_spq = pd.DataFrame()
df_sus = pd.DataFrame()
df_demo = pd.DataFrame()

ai_list, doc_list, ipq_list, sus_list, demo_list = [], [], [], [], []
for pp in to_combine:
    df = pd.read_csv(f'data_intermediate/{pp}/resQues_post_{pp}.csv')
    df_pre = pd.read_csv(f'data_intermediate/{pp}/resQues_pre_{pp}.csv')
    df_sus = pd.read_csv(f'data_intermediate/{pp}/resPostQues_{pp}.csv')
    df_sus.rename(columns={"question_index": "index"}, inplace=True)
    
    # make sure the answer column is numeric
    df["answer_num"] = df["answer"].astype(str).str.extract(r"^(\d+)").astype(float)
    df_pre["answer_num"] = df_pre["answer"].astype(str).str.extract(r"^(\d+)").astype(float)
    df_sus["answer_num"] = df_sus["answer_index"].astype(str).str.extract(r"^(\d+)").astype(float)

    # general demographics
    df_demo = df_pre[df_pre['section']=='0-1']
    demo_list.append(df_demo)
    
    # pre ipq + post ipq
    df_ipq_pre = df_pre[df_pre['section']=='0-1']
    df_ipq_pre[["section"]] = 'pre'
    df_ipq_post = df[df['section']=='2-1']
    df_ipq_post[["section"]] = 'post'
    df_ipq = pd.concat([df_ipq_pre, df_ipq_post], ignore_index=True)
    ipq_list.append(df_ipq)
    
    # AI literacy
    df_ai = df[df['section']=='2-2']
    # ai_list.append(df_ai.groupby(["pp","index"])["answer_num"].mean()
    #                     .groupby("pp").mean().reset_index())
    ai_list.append(df_ai)

    # DoC
    df_doc = df[df['section']=='2-3']
    # doc_list.append(df_doc.groupby(["pp","index"])["answer_num"].mean()
                        # .groupby("pp").mean().reset_index())
    doc_list.append(df_doc)

    # SUS
    sus_list.append(df_sus)
    

df_demo_all = pd.concat(demo_list, ignore_index=True)
df_ipq_all = pd.concat(ipq_list, ignore_index=True)
df_ai_all = pd.concat(ai_list, ignore_index=True)
df_doc_all = pd.concat(doc_list, ignore_index=True)
df_sus_all = pd.concat(sus_list, ignore_index=True)

# save all raw data to csv
df_demo_all.rename(columns={"answer_num": "demo"}, inplace=True)
df_demo_all.to_csv('data_analysis/questionnaire/demo_raw.csv', index=False)

df_ipq_all.rename(columns={"answer_num": "IPQ"}, inplace=True)
df_ipq_all.to_csv('data_analysis/questionnaire/ipq_raw.csv', index=False)

df_doc_all.rename(columns={"answer_num": "DoC"}, inplace=True)
df_doc_all.to_csv('data_analysis/questionnaire/doc_raw.csv', index=False)

df_ai_all.rename(columns={"answer_num": "AI_literacy"}, inplace=True)
df_ai_all.to_csv('data_analysis/questionnaire/ai_raw.csv', index=False)

df_sus_all.rename(columns={"answer_num": "SUS"}, inplace=True)
df_sus_all.to_csv('data_analysis/questionnaire/sus_raw.csv', index=False)

# %%
# question num check
for df, name in zip([df_demo_all, df_ipq_all, df_ai_all, df_doc_all, df_sus_all],
                    ["demo", "ipq", "ai", "doc", "sus"]):
    print(f"{name} question num check:")
    print(df.groupby("pp")["index"].nunique())
    print("\n")

# %%
# standardize DoC, ai literacy, and merge into one csv

df_doc_ave = df_doc_all.groupby("pp")["DoC"].mean().reset_index()
df_ai_ave = df_ai_all.groupby("pp")["AI_literacy"].mean().reset_index()

df_doc_ave['DoC_z'] = df_doc_ave['DoC'].transform(lambda x: (x - x.mean()) / x.std())

df_ai_ave['AI_literacy_z'] = df_ai_ave['AI_literacy'].transform(lambda x: (x - x.mean()) / x.std())


df_traits = pd.merge(df_ai_ave, df_doc_ave, on='pp', how='outer')
df_traits.to_csv('data_analysis/questionnaire/pp_traits.csv', index=False)

# %%
df_traits = pd.read_csv('data_analysis/questionnaire/pp_traits.csv')
wide = pd.read_csv('data_analysis/questionnaire/trial_wise_SoA_cleaned_wide.csv')
df_score = wide.merge(
    df_traits[["pp", "AI_literacy_z", "DoC_z"]],
    on="pp",
    how="left"
)
df_score.to_csv("data_analysis/questionnaire/trial_wise_SoA_with_pp_traits.csv", index=False)

# %%