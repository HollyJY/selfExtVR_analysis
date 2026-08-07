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
def add_significance_bars(ax, p_value, x1, x2, y, significance_level=0.05):
    """Add significance bars to a boxplot."""
    y_offset = 0.5  # Offset for the bar
    ax.plot([x1, x1, x2, x2], [y, y + y_offset, y + y_offset, y], color='black')
    
    # Annotate with asterisks based on p-value
    if p_value < significance_level:
        ax.text((x1 + x2) / 2, y + y_offset + 0.1, '*', fontsize=16, ha='center')
    if p_value < significance_level / 10:
        ax.text((x1 + x2) / 2, y + y_offset + 0.2, '*', fontsize=16, ha='center')
    if p_value < significance_level / 100:
        ax.text((x1 + x2) / 2, y + y_offset + 0.3, '*', fontsize=16, ha='center')

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
add_significance_bars(plt.gca(), p_value=0.0001, x1=0, x2=1, y=df_SoA['rate'].max() + 0.5)
add_significance_bars(plt.gca(), p_value=0.0001, x1=0, x2=2, y=df_SoA['rate'].max() + 1)
add_significance_bars(plt.gca(), p_value=0.0001, x1=1, x2=2, y=df_SoA['rate'].max() + 0.5)
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
add_significance_bars(plt.gca(), p_value=0.007, x1=0, x2=1, y=df_accept['rate'].max() + 0.5)
add_significance_bars(plt.gca(), p_value=0.0001, x1=0, x2=2, y=df_accept['rate'].max() + 1)
add_significance_bars(plt.gca(), p_value=0.0001, x1=1, x2=2, y=df_accept['rate'].max() + 0.5)
plt.ylabel("Acceptance")
plt.title("Acceptance by condition and voice_id")
plt.tight_layout()
plt.savefig('fig/acceptance_boxplot.png', dpi=1000)
plt.show()

# %%
# authorship

df_authorship = df[df['response_type'] == 'Authorship']
plt.figure(figsize=(6, 6))
sns.boxplot(
    data=df_authorship,
    x="condition",
    y="rate",
    hue="voice_id",
    showfliers=True,
    color = "lightpink"
)
plt.ylabel("Authorship")
plt.title("Authorship by condition and voice_id")
add_significance_bars(plt.gca(), p_value=0.007, x1=0, x2=1, y=df_authorship['rate'].max() + 0.5)
add_significance_bars(plt.gca(), p_value=0.0001, x1=0, x2=2, y=df_authorship['rate'].max() + 1)
add_significance_bars(plt.gca(), p_value=0.0001, x1=1, x2=2, y=df_authorship['rate'].max() + 0.5)
plt.tight_layout()
plt.savefig('fig/authorship_boxplot.png', dpi=1000)
plt.show()

# %%
