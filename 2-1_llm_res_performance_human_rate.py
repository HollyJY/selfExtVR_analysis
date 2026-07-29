# %% [markdown]
# get 3 participants' result for checking the LLM performance
# for human rating

# %%
import pandas as pd
import os
import numpy as np

# %%
file = 'data_analysis/all_ans_llm.csv'
df = pd.read_csv(file)

pp_all = list(df['pp'].unique())
# pp_sample = np.random.choice(pp_all, size=3, replace=False)
pp_sample = ['P06', 'P11', 'P26']
print(f"Sampled participants: {pp_sample}")

# %%

df_for_rate = df[df['pp'].isin(pp_sample)]
df_for_rate = df_for_rate.reset_index(drop=True)
display(df_for_rate.head(3))
# %%
df_rate_form = df_for_rate[['context','ans_ori', 'ans_llm', 'condition']].copy()
df_rate_form['transform_correctness'] = np.nan
df_rate_form['style'] = np.nan
df_rate_form['coherence'] = np.nan
df_rate_form['condition'] = df_rate_form['condition'].map({1: 'repeat', 2: 'enhance', 3: 'counter'})

df_rate_form.value_counts('condition')


# %%
df_rate_form.to_csv('data_analysis/llm_res_for_human_rate.csv', index = True)

# %%
