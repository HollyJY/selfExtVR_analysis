# %% [markdown]
# # re-examine the reliability of the scale
# reference: https://pmc.ncbi.nlm.nih.gov/articles/PMC4205511/

# There are different reports about the acceptable values of alpha, ranging from 0.70 to 0.95.

# conclusion @2026-07-28: combine SoNA, SoPA; drop question 6; use SoPA/SoNA as secondary analysis


# %%
import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
import HZutil

# %%
path = "data_analysis/trial_wise_resp_dropped_1.csv"
df = pd.read_csv(path)
df.head(3)

# %%
wide = df.pivot_table(index=["pp", "trial"], columns="question_index", values="answer_index")
wide.head(3)

# %% reliability of positive and negative items separately
#   * [1,4,5,7,8]
#   * [2,3,6]

positive = wide[[1,4,5,7,8]]
negative = wide[[2,3,6]]

alpha, ci = pg.cronbach_alpha(data=positive)
print(f"Cronbach's alpha (positive): {alpha:.3f}")
print(f"Confidence interval: {ci}")

alpha, ci = pg.cronbach_alpha(data=negative)
print(f"Cronbach's alpha (negative): {alpha:.3f}")
print(f"Confidence interval: {ci}")


# %%
li_alpha = []

# drop 1, positive
for col in positive.columns:
    left = positive.drop(columns=[col])
    alpha, ci = pg.cronbach_alpha(data=left)
    li_alpha.append(["positive", int(col), alpha, ci])

# drop 1, negative
for col in negative.columns:
    left = negative.drop(columns=[col])
    alpha, ci = pg.cronbach_alpha(data=left)
    li_alpha.append(["negative", int(col), alpha, ci])

df = pd.DataFrame(li_alpha, columns=["SoA", "dropped", "alpha", "ci"])
# df.head(3)

# %%

sns.scatterplot(data=df, x="dropped", y="alpha", hue="SoA")
plt.xticks(ticks=[1,2,3,4,5,6,7,8], labels=[1,2,3,4,5,6,7,8])
plt.xlabel("Dropped question index")
plt.title("Cronbach's alpha after dropping each question")
plt.tight_layout()
plt.savefig("fig/cronbach_alpha_dropped.png", dpi=1000)
plt.show()


# %%
# what if - negative items are reverse coded?
wide[[2,3,6]] = 8 - wide[[2,3,6]]

alpha, ci = pg.cronbach_alpha(data=wide)
print(f"Cronbach's alpha (negative items reverse coded): {alpha:.3f}")
print(f"Confidence interval: {ci}")

li_alpha_reversed = []

for col in wide.columns:
    left = wide.drop(columns=[col])
    alpha, ci = pg.cronbach_alpha(data=left)
    li_alpha_reversed.append(["", int(col), alpha, ci])

df_reversed = pd.DataFrame(li_alpha_reversed, columns=["SoA", "dropped", "alpha", "ci"])
df_reversed["SoA"] = df["SoA"]
# df_reversed.head(3)

sns.scatterplot(data=df_reversed, x="dropped", y="alpha", hue="SoA")
plt.xticks(ticks=[1,2,3,4,5,6,7,8], labels=[1,2,3,4,5,6,7,8])
plt.xlabel("Dropped question index")
plt.title("Cronbach's alpha after dropping each question (negative items reverse coded)")
plt.tight_layout()
plt.savefig("fig/cronbach_alpha_dropped_reversed.png", dpi=1000)
plt.show()

# %%
# item correlation for Ques 6, in negative items
from scipy.stats import pearsonr

for col in negative.columns:
    rest = negative[[c for c in negative.columns if c != col]].mean(axis=1)
    r, p = pearsonr(negative[col], rest)
    print(f"{col}: r = {r:.3f}, p = {p:.3g}")

# "0.20–0.30 Weak but often usable"


# %%
df = pd.read_csv("data_analysis/trial_wise_resp_dropped_1.csv")
df.drop(df[df['question_index']==6].index, inplace=True)
df.to_csv("data_analysis/trial_wise_resp_dropped_2_ques6.csv", index=False)
# %%
