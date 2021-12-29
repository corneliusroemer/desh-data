# %%
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns

# %%
df = pd.read_csv(
    "data/meta_lineages.csv",
    index_col=0,
    parse_dates=[1, 3],
    infer_datetime_format=True,
    cache_dates=True,
    dtype={
        "SEQ_REASON": "category",
        "SENDING_LAB_PC": "category",
        "SEQUENCING_LAB_PC": "category",
        "lineage": "category",
        "scorpio_call": "category",
    },
)
df.rename(
    columns={
        "DATE_DRAW": "date",
        "PROCESSING_DATE": "processing_date",
        "SEQ_REASON": "reason",
        "SENDING_LAB_PC": "sending_pc",
        "SEQUENCING_LAB_PC": "sequencing_pc",
        "lineage": "lineage",
        "scorpio_call": "scorpio",
    },
    inplace=True,
)
# %%
df["delay"] = (df["processing_date"] - df["date"]).dt.days
df.delay.describe()

# %%
# Inspired by https://stackoverflow.com/a/30305331/7483211
sns.set_theme()
max_days = 25
bins = np.arange(0, max_days + 1, 1)

fig, ax = plt.subplots(figsize=(7, 4))
_, bins, patches = plt.hist(np.clip(df.delay, bins[0], bins[-1]), density=True, bins=bins)
xlabels = bins[0:-1].astype(str)
xlabels[-1] += "+"

N_labels = len(xlabels)
plt.xlim([0, max_days])
plt.xticks(np.arange(N_labels) + 0.5)
ax.set_xticklabels(xlabels)

nice_formatter = ticker.FuncFormatter(
    lambda y, _: f'{ np.format_float_positional(100*y, trim="-", precision=6).rstrip(".")}%'
)
ax.yaxis.set_major_formatter(nice_formatter)

ax.set_xlabel("Delay between sample draw and sequence processing (days)")
ax.set_ylabel("Fraction of sequences")
ax.set_title("Time between sample draw and sequence processing")
plt.figtext(
    0.97,
    -0.02,
    f"Datenstand: {str(dt.date.today())}"
    + " | Datenquelle: RKI Sequenzdaten https://doi.org/10.5281/zenodo.5139363"
    + " | Analyse: @CorneliusRoemer",
    size=6,
    va="bottom",
    ha="right",
)
fig.tight_layout()
fig.savefig("plots/sequencing_delay.png", dpi=200, bbox_inches="tight", pad_inches=0.3)
