#%%
import datetime as dt

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
def plot_omicron_share(df,reason,scale):
    df_reason = df[df.date > '2021-11-01']

    if reason in ['N', 'Y']:
        df_reason = df[df.reason == reason]
    elif reason == 'NX':
        df_reason = df[df.reason.isin(['N','X'])]


    daily_omicrons = df_reason.resample('D',on='date')['lineage'].apply(lambda x: (x == 'BA.1').sum())
    daily_all = df_reason.resample('D',on='date')['lineage'].count()

    plot_df = pd.concat({'omicrons':daily_omicrons,'all': daily_all}, axis=1)
    plot_df['omicron_share'] = plot_df['omicrons']/plot_df['all']

    fig, ax = plt.subplots(num=None, figsize=(6.75, 4), facecolor='w', edgecolor='k')
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.25)
    sns.scatterplot(data=plot_df['20211118':], x="date", y="omicron_share", hue="all", size="all")
    fig.text(0.51, 0.1, f"Datenstand: {str(dt.date.today())} | Datenquelle: RKI Sequenzdaten https://doi.org/10.5281/zenodo.5139363 | Viz: @CorneliusRoemer", size=6, va="bottom", ha="center")

    if scale == 'logit':
        ax.set_yscale('logit')
        ax.set_ylabel('Omikron-Anteil (Logit-Skala)')
    else:
        ax.set_ylabel('Omikron-Anteil')

    ax.set_xlabel('Proben-Datum')

    if reason in [None,'all']:
        title = "allen Proben"
    elif reason == 'N':
        title = "der repräsentativen Surveillance"
    else:
        title = f"Proben vom Typ {reason}"
    ax.set_title(f'Omikron-Anteil in Deutschland in {title}')

    ax.get_legend().set_title('Proben-Anzahl')
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=1.0))
    ax.grid(True, which='major', linewidth=0.25)
    ax.grid(True, which='minor', linewidth=0.1)
    ax.set_axisbelow(True)

    if scale == 'logit':
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{float(f"{100*y:.1g}"):g}%'))
    else:
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:.0%}'))

    fig.savefig(f'plots/omicron_{reason}_{scale}.png', dpi=300)
#%%
plot_omicron_share(df,'N','logit')
plot_omicron_share(df,'N','linear')

plot_omicron_share(df,'all','logit')
plot_omicron_share(df,'all','linear')

plot_omicron_share(df,'NX','logit')
plot_omicron_share(df,'NX','linear')

# %%
