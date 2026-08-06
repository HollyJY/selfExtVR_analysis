# %% [markdown]
# # trial wise responses analysis, visualization

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import HZutil

# %% 
path = 'data_analysis/trial_wise_SoA_cleaned_long.csv'
df = pd.read_csv(path)
display(df.head(3))

# %%
# primary: SoA

plt.subplots(1, 2, figsize=(10, 6), gridspec_kw={"width_ratios": [1, 1]},sharey=False)
# plt.suptitle('SoA and Acceptance scores by content')

plt.subplot(1, 2, 1)
df_SoA = df[df['response_type'] == 'SoA']

sns.boxplot(
    data=df_SoA,
    x="condition",
    y="rate",
    hue="voice_id",
    showfliers=True,
    color = 'red'
)
plt.ylabel("SoA")
plt.title("SoA by condition and voice_id")

plt.subplot(1, 2, 2)
df_accept = df[df['response_type'] == 'Accept']
sns.boxplot(
    data=df_accept,
    x="condition",
    y="rate",
    hue="voice_id",
    showfliers=True,
    color = "lightblue"
)
plt.ylabel("Acceptance")
plt.title("Acceptance by condition and voice_id")
plt.tight_layout()
plt.savefig('fig/acceptance_boxplot.png', dpi=1000)
plt.show()

# %%
# authorship
# %%
