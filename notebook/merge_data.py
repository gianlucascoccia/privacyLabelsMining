# %% Imports

import pandas as pd

# %% Set path fopr output file

OUT_FILE = '../data/processed/apps.csv'

# %% Load raw data files

app_list = pd.read_csv('../data/raw/top_apps_list.csv', delimiter=';')
store_data = pd.read_csv('../data/raw/apps_store_data.csv', delimiter=';')
labels = pd.read_csv('../data/raw/privacy_labels.csv', delimiter=';')

# %% Drop NA rows and duplicates

app_list = app_list.dropna(how='all')
app_list = app_list.drop_duplicates(subset=['name'])

store_data = store_data.dropna(how='all')
store_data = store_data.drop_duplicates(subset=['appId'])

labels = labels.dropna(how='all')
labels = labels.drop_duplicates(subset=['id'])

# %% Merge data 

apps = pd.merge(app_list, labels, how='left', on='id')
apps = pd.merge(apps, store_data, how='left', on='id')
apps = apps.dropna(subset=['tLocation'])

# %% Write output

apps.to_csv(OUT_FILE, sep=';')

# %%
