# %% Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% Load raw data files

apps = pd.read_csv('../data/processed/apps_top1000_all.csv', delimiter=';') 

# %% Helper vars

data_types = ['Health & Fitness', 'Location', 'Contact Info', 'Diagnostics', 'Sensitive Info', 'Usage Data', 'Browsing History', 'Contacts', 'Purchases', 'Identifiers', 'Other Data', 'Financial Info', 'Search History', 'User Content']

tracking_colnames = ['t' + x.replace(' ', '') for x in data_types]
linked_colnames = ['l' + x.replace(' ', '') for x in data_types]
unlinked_colnames = ['u' + x.replace(' ', '') for x in data_types]

# %% Counts of tracking, linked and unlinked

apps['tracking_count'] = apps[tracking_colnames].sum(axis=1)
apps['linked_count'] = apps[linked_colnames].sum(axis=1)
apps['unlinked_count'] = apps[unlinked_colnames].sum(axis=1)
apps['all_count'] = apps['tracking_count'] + apps['linked_count'] + apps['unlinked_count']

# %% Flags of types of data usage

apps['has_tracking'] = apps['tracking_count'].apply(lambda x: x > 0)
apps['has_linked'] = apps['linked_count'].apply(lambda x: x > 0)        
apps['has_unlinked'] = apps['unlinked_count'].apply(lambda x: x > 0)
apps['has_any'] = apps['all_count'].apply(lambda x: x > 0)        

# %% Divide in free and paid

apps_free = apps[apps['free'] == True] 
apps_paid = apps[apps['free'] == False] 

apps_types = [('free', apps_free), ('paid', apps_paid)]

# %% Summary stats

for df in apps_types: 
    print("{} {} apps".format(df[0], len(df[1])))

for df in apps_types:
    print('---------------- {} -----------------'.format(df[0]))
    print('#### Usages count ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(round(df[1]['tracking_count'].sum(),2), round(df[1]['linked_count'].sum(),2), round(df[1]['unlinked_count'].sum(),2), round(df[1]['all_count'].sum(),2)))

    print('#### Median ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(round(df[1]['tracking_count'].median(),2), round(df[1]['linked_count'].median(),2), round(df[1]['unlinked_count'].median(),2), round(df[1]['all_count'].median(),2)))

    print('#### Mean ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(round(df[1]['tracking_count'].mean(),2), round(df[1]['linked_count'].mean(),2), round(df[1]['unlinked_count'].mean(),2), round(df[1]['all_count'].mean(),2)))

    print('#### SD ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(round(df[1]['tracking_count'].std(),2), round(df[1]['linked_count'].std(),2), round(df[1]['unlinked_count'].std(),2), round(df[1]['all_count'].std(),2)))

# %% Percentage of apps using tracking, linked, unlinked data

for df in apps_types: 
    t_percentage = sum(df[1]['has_tracking']) / len(df[1]) * 100
    l_percentage = sum(df[1]['has_linked']) / len(df[1]) * 100
    u_percentage = sum(df[1]['has_unlinked']) / len(df[1]) * 100
    any_percentage = sum(df[1]['has_any']) / len(df[1]) * 100

    print("In the {} apps there are {}% using tracking data, {}% using linked data, and {}% using unlinked data, and {}% using data of any kind".format(df[0], round(t_percentage,2), round(l_percentage,2), round(u_percentage,2), round(any_percentage,2) ))

# %% Correlations
apps.corr(method='spearman').to_csv('correlation.csv')

# %%
