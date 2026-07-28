# %% [markdown]
# # trial wise responses preprocess
# - [x] drop incomplete trials (std = 0 for all questions)
# - [ ] llm failure
# - [x] calculate SoPA, SoNA, acceptance, SoA

# %%
import pandas as pd

# %%
# ## read in the data, long table
df = pd.read_csv('data_analysis/trial_wise_resp.csv')
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

df.to_csv('data_analysis/trial_wise_response_dropped_1.csv', index=False)
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

# %%
