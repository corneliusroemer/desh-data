#%%
import datetime as dt
import locale

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns

#%%
df = pd.read_csv(
    'data/meta_lineages.csv',
    index_col=0,
    parse_dates=[1,3],
    infer_datetime_format=True,
    cache_dates=True,
    dtype = {'SEQ_REASON': 'category',
             'SENDING_LAB_PC': 'category',
             'SEQUENCING_LAB_PC': 'category',
             'lineage': 'category',
             'scorpio_call': 'category'
             }
)
#%%
df.rename(columns={
    'DATE_DRAW': 'date',
    'PROCESSING_DATE': 'processing_date',
    'SEQ_REASON': 'reason',
    'SENDING_LAB_PC': 'sending_pc',
    'SEQUENCING_LAB_PC': 'sequencing_pc',
    'lineage': 'lineage',
    'scorpio_call': 'scorpio'
    },
    inplace=True
)
#%%
# Restrict to recent samples
df = df[df.date > '2021-11-01']
#%%
# Restrict to surveillance samples
df = df[df.reason == 'N']
#%%
daily_omicrons = df.resample('D',on='date')['lineage'].apply(lambda x: (x == 'BA.1').sum())
daily_all = df.resample('D',on='date')['lineage'].count()
#%%
plot_df = pd.concat({'omicrons':daily_omicrons,'all': daily_all}, axis=1)
plot_df['omicron_share'] = plot_df['omicrons']/plot_df['all']
#%%
# Logit plot
# locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
fig, ax = plt.subplots(num=None, figsize=(6.75, 4), facecolor='w', edgecolor='k')
sns.scatterplot(data=plot_df['20211118':], x="date", y="omicron_share", hue="all", size="all")
plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.25)
fig.text(0.52, 0.1, f"Datenstand: {str(dt.date.today())} | Datenquelle: RKI Sequenzdaten https://doi.org/10.5281/zenodo.5139363 | Viz: @CorneliusRoemer", size=6, va="bottom", ha="center")
ax.set_yscale('logit')
ax.set_ylabel('Omikron-Anteil (Logit-Skala)')
ax.tick_params(axis='y',labelsize=12)
ax.set_xlabel('Proben-Datum')
ax.set_title('Omikron-Anteil in Deutschland in der repräsentativen Surveillance')
ax.get_legend().set_title('Proben-Anzahl')
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
fig.savefig('plots/omicron_logit.png', dpi=300)
# %%
# Linear plot
fig, ax = plt.subplots(num=None, figsize=(6.75, 4), facecolor='w', edgecolor='k')
sns.scatterplot(data=plot_df['20211118':], x="date", y="omicron_share", hue="all", size="all")
plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.25)
fig.text(0.52, 0.1, f"Datenstand: {str(dt.date.today())} | Datenquelle: RKI Sequenzdaten https://doi.org/10.5281/zenodo.5139363 | Viz: @CorneliusRoemer", size=6, va="bottom", ha="center")
ax.set_ylabel('Omikron-Anteil')
ax.set_xlabel('Proben-Datum')
ax.set_title('Omikron-Anteil in Deutschland in der repräsentativen Surveillance')
ax.get_legend().set_title('Proben-Anzahl')
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:.0%}'))
fig.savefig('plots/omicron_linear.png', dpi=300)
# %%
