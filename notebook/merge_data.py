# %% Imports

import pandas as pd

# %% Set path for output file

OUT_FILE = '../data/processed/apps_top1000_all.csv'

# %% Load raw data files

app_list_free = pd.read_csv('../data/raw/top_1000_apps_free.csv', delimiter=';')
app_list_top = pd.read_csv('../data/raw/top_1000_apps_top_grossing.csv', delimiter=';')

# Rename cols to not lose information when merging
app_list_free = app_list_free.rename(columns={'top_chart_position': 'top_chart_position_free'}) 
app_list_top = app_list_top.rename(columns={'top_chart_position': 'top_chart_position_grossing'}) 

store_data_free = pd.read_csv('../data/raw/top_1000_apps_free_store_data.csv', delimiter=';')
store_data_top = pd.read_csv('../data/raw/top_1000_apps_top_grossing_store_data.csv', delimiter=';')

labels_free = pd.read_csv('../data/raw/privacy_labels_top_1000_free.csv', delimiter=';')
labels_top = pd.read_csv('../data/raw/privacy_labels_top_1000_top_grossing.csv', delimiter=';')

usages_free = pd.read_csv('../data/raw/top_1000_apps_free_purposes.csv', delimiter=';')
usages_top = pd.read_csv('../data/raw/top_1000_apps_top_grossing_purposes.csv', delimiter=';')


# %% Merge data

app_list = pd.concat([app_list_free, app_list_top], ignore_index=False, sort=False)
store_data = pd.concat([store_data_free, store_data_top], ignore_index=False, sort=False)
labels = pd.concat([labels_free, labels_top], ignore_index=False, sort=False)
usages = pd.concat([usages_free, usages_top], ignore_index=False, sort=False)

# %% Drop NA rows and duplicates

app_list = app_list.dropna(how='all')
app_list = app_list.drop_duplicates(subset=['name'])

store_data = store_data.dropna(how='all')
store_data = store_data.drop_duplicates(subset=['appId'])

labels = labels.dropna(how='all')
labels = labels.drop_duplicates(subset=['id'])

usages = usages.dropna(how='all')
usages = usages.drop_duplicates(subset=['id'])

# %% Merge data 

apps = pd.merge(app_list, labels, how='left', on='id')
apps = pd.merge(apps, store_data, how='left', on='id')
apps = pd.merge(apps, usages, how='left', on='id')
apps = apps.dropna(subset=['tLocation'])

# %% Drop apps last updated prior to 15 December 2020 (iOS 14.3 release date)

pre = len(apps)
apps = apps[(apps['updated'] >= '2020-12-15')]
post = len(apps)
print("{} rows survived from {}, {} were discarded".format(post, pre, pre - post))

# %% Write output

apps.to_csv(OUT_FILE, sep=';')

# %%
