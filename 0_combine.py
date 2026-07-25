# %% [markdown]
# ### what to do in the script
# 1. put all trials info / txt -> 1 csv file
# 2. put all questionnaire responses -> 1 csv file
# 
# ---
# 
# under 1 P[xx]_session/
# - speech_response: expInfo -> for each trial, scene, condition, original answer, modified outputs <== HMD(expInfo) + server (speech content)
# - eye_tracking <== HMD
# - scale_response: expInfo + resScale <== HMD
# - resPostQues <== HMD

# %%
import string

import pandas as pd
import os
import sys
import shutil
from pathlib import Path

# %%
# read all existing folders in data_extSelf, list the ones that haven't been processed, and combine the processed ones into one file

to_combine = [folder for folder in os.listdir('data_raw/HMD') if folder.startswith('P')]
# to_combine = [folder for folder in to_combine if not os.path.exists(f'data_intermediate/{folder}')]
print(to_combine)
print(len(to_combine))

# %%
def read_asr(row):
    session = row["pp"]
    trial = int(row["trial"])

    path = os.path.join(
        "data_extSelf_server",
        session,
        f"trial_{trial:03d}",
        "user_1B_asr.txt"
    )

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()
    
def read_llm(row):
    session = row["pp"]
    trial = int(row["trial"])

    path = os.path.join(
        "data_extSelf_server",
        session,
        f"trial_{trial:03d}",
        "user_2B_llm.txt"
    )

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

# %%
for pp in to_combine:
    pp_id = pp.split("_")[0]  # extract the participant ID from the folder name
    # create folder, copy #1 - expInfo.csv, questionnaires.csv, and #2 - eyeData.csv, and #3 - gazeData.csv into the new folder
    if not os.path.exists(f'data_intermediate/{pp_id}'):
        os.makedirs(f'data_intermediate/{pp_id}')

    df = pd.read_csv(f'data_raw/HMD/{pp}/expInfo_{pp}.csv')
    df['pp'] = pp_id
    df.to_csv(f'data_intermediate/{pp_id}/expInfo_{pp_id}.csv', index=False)

    src = Path(f'data_raw/HMD/{pp}')
    dst = Path(f'data_intermediate/{pp_id}')

    patterns = [
        "*_log.csv",
        "*_log_eye.csv",
        "*_log_eye_raw.csv",
        # "res*_session.csv",
    ]

    for pattern in patterns:
        for file in src.glob(pattern):
            shutil.copy2(file, dst / file.name)

    for file in src.glob("res*_session.csv"):
        df = pd.read_csv(file)
        df['pp'] = pp_id
        df = df.tail(108)  # only take last 108 rows
        df.to_csv(f'{dst}/' + file.name.split('_')[0] + f'_{pp_id}.csv', index=False)

    # file #2: combine the textual outputs
    # read expInfo

    df = pd.read_csv(f'data_intermediate/{pp_id}/expInfo_{pp_id}.csv')
    df.head(3)
    df['ans_ori'] = df.apply(read_asr, axis=1)
    df['ans_llm'] = df.apply(read_llm, axis=1)
    df['pp_id'] = pp_id
    df.to_csv(f'{dst}/ans_llm_{pp_id}.csv', index=False)

    # file #3: pre+post questionnaire data
    src = Path(f'data_raw/server/{pp}')
    patterns = [
        "resQues_*.csv",
        # "extself*.m4a",
        ]
    for pattern in patterns:
        for file in src.glob(pattern):
            df = pd.read_csv(file)
            df['pp'] = pp_id
            df.to_csv(f'{dst}/' + 'resQues_' + file.name.split('_')[2].split('.')[0] + f'_{pp_id}.csv', index=False)

    # file #4: interviews
    src = Path(f'data_raw/server/{pp}')
    dst = Path(f'data_raw/interviews/{pp_id}/audio')
    if not os.path.exists(f'data_raw/interviews/{pp_id}/audio'):
        os.makedirs(f'data_raw/interviews/{pp_id}/audio')
    patterns = [
        "*.m4a",
    ]
    for pattern in patterns:
        for file in src.glob(pattern):
            shutil.copy2(file, dst / f"{pp_id}_interview_raw.m4a")

# %%
# concatenate all trial wise responses into one
to_concat = [folder for folder in os.listdir('data_intermediate') if folder.startswith('P')]
for pp in to_concat:
    pp_id = pp.split("_")[0]  # extract the participant ID from the folder name
    
    df = pd.read_csv(f'data_intermediate/{pp_id}/ans_llm_{pp_id}.csv')
    df['pp'] = pp_id
    if 'all_df_llm' in locals():
        all_df_llm = pd.concat([all_df_llm, df], ignore_index=True)
    else:
        all_df_llm = df
all_df_llm.to_csv('data_analysis/all_ans_llm.csv', index=False)

for pp in to_concat:
    pp_id = pp.split("_")[0]  # extract the participant ID from the folder name
    
    df = pd.read_csv(f'data_intermediate/{pp_id}/expInfo_{pp_id}.csv')
    df['pp'] = pp_id
    if 'all_df_expInfo' in locals():
        all_df_expInfo = pd.concat([all_df_expInfo, df], ignore_index=True)
    else:
        all_df_expInfo = df
all_df_expInfo.to_csv('data_analysis/all_expInfo.csv', index=False)

for pp in to_concat:
    pp_id = pp.split("_")[0]  # extract the participant ID from the folder name
    
    df = pd.read_csv(f'data_intermediate/{pp_id}/resScale_{pp_id}.csv')
    df['pp'] = pp_id
    if 'all_df_resScale' in locals():
        all_df_resScale = pd.concat([all_df_resScale, df], ignore_index=True)
    else:
        all_df_resScale = df
all_df_resScale.to_csv('data_analysis/all_resScale_session.csv', index=False)

# %%
# combine trial wise responses + conditions into one file
# long table
to_combine = [folder for folder in os.listdir('data_raw/HMD') if folder.startswith('P')]

df_all_scale = pd.read_csv('data_analysis/all_resScale_session.csv')
df_all_expInfo = pd.read_csv('data_analysis/all_expInfo.csv')

def get_condition(row):
    pp = row['pp']
    trial = row['trial']
    # df_pp = df_all_scale[df_all_scale['pp'] == pp]
    condition = df_all_expInfo[(df_all_expInfo['pp'] == pp) & (df_all_expInfo['trial'] == trial)]['condition'].values
    if len(condition) > 0:
        cond = 'repeat' if condition[0] == 1 else ('enhance' if condition[0] == 2 else 'counter')
        return cond
    else:
        return None
    
def get_voice_id(row):
    pp = row['pp']
    trial = row['trial']
    df_pp = df_all_scale[df_all_scale['pp'] == pp]
    voice_id = df_all_expInfo[(df_all_expInfo['pp'] == pp) & (df_all_expInfo['trial'] == trial)]['raw_voice_id'].values
    if voice_id[0] == 'clone':
        return 'clone'
    else:
        return 'robotic'
    
df_all_scale['condition'] = df_all_scale.apply(get_condition, axis=1)
df_all_scale['voice_id'] = df_all_scale.apply(get_voice_id, axis=1)

df_all_scale.to_csv('data_analysis/trial_wise_responses.csv', index=False)

# %%
