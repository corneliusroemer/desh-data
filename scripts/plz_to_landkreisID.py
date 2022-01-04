# %%
import numpy as np
import pandas as pd
#%%
plz_raw = pd.read_csv(
    "https://raw.githubusercontent.com/zauberware/postal-codes-json-xml-csv/master/data/DE/zipcodes.de.csv",
    sep=",",
    dtype=str,
)
df = plz_raw.groupby('zipcode').first().reset_index()
# %%

seq = pd.read_csv("data/meta_lineages.csv", sep=",", dtype=str)
seq.dropna(subset=["SENDING_LAB_PC"], inplace=True)
sending = seq.SENDING_LAB_PC.unique()
plzs_to_impute = sending[~np.isin(sending,df.zipcode.unique())]
plzs_to_impute
#%%
# df[df.zipcode == '17475']
# np.isin(sending,'17475')
#%%
def nearest_neighbour_plz(df, plz):
    # Find nearest neighbours
    for i in range(1,6):
        nearest_neighbours = df.zipcode[df.zipcode.apply(lambda x: x[:-i]) == plz[:-i]]
        if len(nearest_neighbours) > 0:
            nn_df = pd.DataFrame({'zipcode':nearest_neighbours})
            nn_df['distance'] = np.abs(nearest_neighbours.astype(int)-int(plz))
            return nn_df.sort_values('distance').zipcode.iloc[0]
nearest_neighbour_plz(df, '01000')
#%%
imputed_zips = pd.DataFrame({'zipcode': plzs_to_impute})
imputed_zips['imputed'] = imputed_zips.zipcode.apply(lambda x: nearest_neighbour_plz(df,x))

imputed_zips_joined = imputed_zips.join(df.set_index('zipcode'), on='imputed').drop({'imputed'}, axis=1)
df = df.append(imputed_zips_joined).reset_index(drop=True)
#%%
# Restrict to zips that appear in the data
df = df[df.zipcode.isin(sending)]
#%%
incidence = pd.read_csv("data/kreis_inzidenz.csv", sep=",", dtype={"IdMeldeLandkreis": str})
incidence[incidence.IdMeldeLandkreis.isin(df.zipcode.unique())]
#%%
# Fixed by adding manual Land Berlin -> 11000 and Eisenach -> Wartburgkreis
df[~df.community_code.isin(incidence.IdMeldeLandkreis.unique())]
# %%
df['inc_2021-11-25'] = df.community_code.apply(lambda x: incidence.loc[incidence.IdMeldeLandkreis == x, '2021-11-25'].values[0])
df['inc_2021-12-10'] = df.community_code.apply(lambda x: incidence.loc[incidence.IdMeldeLandkreis == x, '2021-12-10'].values[0])
df['inc_2021-12-20'] = df.community_code.apply(lambda x: incidence.loc[incidence.IdMeldeLandkreis == x, '2021-12-20'].values[0])
df.to_csv("data/plz_metadata.csv", index=False)
# %%

# %%
