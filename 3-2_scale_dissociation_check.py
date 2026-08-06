# %% [markdown]
# # Scale Dissociation Check
# - Agency-Acceptance relationships
# - Authorship vs. Acceptance (kept as distinct items)
# - Descriptive stats: high agency <-> low acceptance; low agency <-> high acceptance; also for authorship 
# - 2 x correlation plots

# ---
# stats
# - [ ] (what test to make)[https://yatani.jp/teaching/doku.php?id=hcistats:start]
# - [ ] + corrections, multiple comparisons, etc.
# - [?] what do i use for median split? (median, mean, quantile, etc.) 3/4?

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
import HZutil

# %%
# Load the data
df = pd.read_csv("data_analysis/trial_wise_SoA_with_pp_traits.csv")
df.head(3)

# %%
# data, form -> high / low agency, high / low authorship, high / low acceptance
li_keys = ["SoA", "Authorship", "Accept"]
for key in li_keys:
    median = df[key].median()         # use median for split
    # median = 5 if key == "Accept" else 3  # for Accept, use 5 as the threshold
    df[key + "_high"] = df[key] > median
    df[key + "_low"] = df[key] <= median
df.head(3)

# %%
# 1: Check the correlation between Agency and Acceptance
agency_acceptance = pg.rm_corr(
    data=df,
    x="SoA",
    y="Accept",
    subject="pp"
)

print(agency_acceptance)

# plot
plt.figure(figsize=(6, 6))
sns.regplot(
    data=df,
    x="SoA",
    y="Accept",
    scatter_kws={"alpha":0.3}
)
plt.title("rmcorr: Agency vs. Acceptance, \nr_rm = {:.2f}, p = {:.2e}".format(agency_acceptance["r"].values[0], agency_acceptance["pval"].values[0]))
plt.tight_layout()
# plt.savefig("fig/3-2_scale_dissociation_check_agency_acceptance.png", dpi=1000)
plt.show()

# %%
# 2: Check the correlation between Authorship and Acceptance
authorship_acceptance = pg.rm_corr(
    data=df,
    x="Authorship",
    y="Accept",
    subject="pp"
)

print(authorship_acceptance)

# plot
plt.figure(figsize=(6, 6))
sns.regplot(
    data=df,
    x="Authorship",
    y="Accept",
    scatter_kws={"alpha":0.3},
    color = "blue"
)
plt.title("rmcorr: Authorship vs. Acceptance, \nr_rm = {:.2f}, p = {:.2e}".format(authorship_acceptance["r"].values[0], authorship_acceptance["pval"].values[0]))
plt.tight_layout()
# plt.savefig("fig/3-2_scale_dissociation_check_authorship_acceptance.png", dpi=1000)
plt.show()

# %%
# 3: Descriptive high/low split
def descriptive_split(df, key1, key2):
    split = df.groupby([key1 + "_high", key2 + "_high"]).size().reset_index(name="count")
    split[key1 + "_high"] = split[key1 + "_high"].map({True: "High " + key1, False: "Low " + key1})
    split[key2 + "_high"] = split[key2 + "_high"].map({True: "High " + key2, False: "Low " + key2})
    split.rename(columns={key1 + "_high": key1, key2 + "_high": key2}, inplace=True)
    return split

# for different conditions, we can use a bar plot to visualize the counts
li_combinations = [("SoA", "Accept"), 
                ("Authorship", "Accept"),
                ("SoA", "Authorship"),
]
for key1, key2 in li_combinations:
    split = descriptive_split(df, key1, key2)
    plt.figure(figsize=(6, 4))
    sns.barplot(data=split, x=key1, y="count", hue=key2)
    plt.xticks([0, 1], [f"Low {key1}", f"High {key1}"])
    plt.title(f"Descriptive Split: {key1} vs. {key2}")
    plt.tight_layout()
    # plt.savefig(f"fig/3-2_descriptive_split_{key1}_{key2}.png", dpi=1000)
    plt.show()
    
# %%
# for separate conditions, calculate do the count
conditions = df.condition.unique()
voice_ids = df.voice_id.unique()
# print(f"Conditions: {conditions}, Voice IDs: {voice_ids}")

df_condition_counts = pd.DataFrame(columns=["condition", "voice_id", "key1", "key2", "count"])

for condition in conditions:
    for voice_id in voice_ids:
        df_condition_voice = df[(df.condition == condition) & (df.voice_id == voice_id)]
        for key1, key2 in li_combinations:
            split = descriptive_split(df_condition_voice, key1, key2)
            split["condition"] = condition
            split["voice_id"] = voice_id
            split["key1"] = key1
            split["key2"] = key2
            df_condition_counts = pd.concat([df_condition_counts, split], ignore_index=True)
            
df_condition_counts.head(3)
# %%
# count only mismatch cases (high/low)
for key1, key2 in li_combinations:
    df_condition_counts[key1 + "_" + key2 + "_mismatch"] = df_condition_counts[(df_condition_counts["key1"] != df_condition_counts["key2"])]
df_condition_counts.groupby(["condition","voice_id"]).sum().reset_index()
# %%
