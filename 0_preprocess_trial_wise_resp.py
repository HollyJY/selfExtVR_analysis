# %% [markdown]
# # trial wise responses preprocess
# - [x] drop incomplete trials (std = 0 for all questions)
# - [ ] llm failure
# - [ ] drop quesion 6 (negative item) for reliability analysis
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
# drop question 6 (negative item) for reliability analysis
df = pd.read_csv("data_analysis/trial_wise_resp_dropped_1.csv")
df.drop(df[df['question_index']==6].index, inplace=True)
df.to_csv("data_analysis/trial_wise_resp_dropped_2_ques6.csv", index=False)

# %% 
# calculate SoPA, SoNA, acceptance, SoPA
wide['SoPA'] = wide[[1, 4, 5, 7, 8]].mean(axis=1)
wide['SoNA'] = wide[[2, 3]].mean(axis=1) # drop question 6

wide['Accept'] = wide[[9]]

display(wide.head(6))

# FIXME: how to calculate SoA? => reverse, 8-negative rating, average
# wide['SoA'] = wide['SoPA'] - wide['SoNA']
for i in [2,3]:
    wide[i] = 8 - wide[i]  # reverse
wide['SoA'] = wide[[1, 2, 3, 4, 5, 7, 8]].mean(axis=1) # drop ques 6

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
