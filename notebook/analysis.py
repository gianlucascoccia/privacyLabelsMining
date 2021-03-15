# %% Imports

import pandas as pd

# %% Load raw data files

apps = pd.read_csv('../data/processed/apps_top1000_all.csv', delimiter=';') 

# %% Divide in free and paid

apps_free = apps[apps['free'] == True] 
apps_paid = apps[apps['free'] == False] 

# %% Helper vars

data_types = ['Health & Fitness', 'Location', 'Contact Info', 'Diagnostics', 'Sensitive Info', 'Usage Data', 'Browsing History', 'Contacts', 'Purchases', 'Identifiers', 'Other Data', 'Financial Info', 'Search History', 'User Content']

tracking_colnames = ['t' + x.replace(' ', '') for x in data_types]
linked_colnames = ['l' + x.replace(' ', '') for x in data_types]
unlinked_colnames = ['u' + x.replace(' ', '') for x in data_types]

apps = [('free', apps_free), ('paid', apps_paid)]

# %% Counts of tracking, linked and unlinked

for df in apps:
    df[1]['tracking_count'] = df[1][tracking_colnames].sum(axis=1)
    df[1]['linked_count'] = df[1][linked_colnames].sum(axis=1)
    df[1]['unlinked_count'] = df[1][unlinked_colnames].sum(axis=1)
    df[1]['all_count'] = df[1]['tracking_count'] + df[1]['linked_count'] + df[1]['unlinked_count']

# %% Flags of types of data usage

for df in apps:
    df[1]['has_tracking'] = df[1]['tracking_count'].apply(lambda x: x > 0)
    df[1]['has_linked'] = df[1]['linked_count'].apply(lambda x: x > 0)        
    df[1]['has_unlinked'] = df[1]['unlinked_count'].apply(lambda x: x > 0)
    df[1]['has_any'] = df[1]['all_count'].apply(lambda x: x > 0)        

# %% Summary stats

## TODO: top-grossing non è paid, vanno separate free da paid (conviene fare merger in un unico csv dei due files)

for df in apps: 
    print("{} {} apps".format(df[0], len(df[1])))

for df in apps:
    print('---------------- {} -----------------'.format(df[0]))
    print('#### Usages count ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(df[1]['tracking_count'].sum(), df[1]['linked_count'].sum(), df[1]['unlinked_count'].sum(), df[1]['all_count'].sum()))

    print('#### Median ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(df[1]['tracking_count'].median(), df[1]['linked_count'].median(), df[1]['unlinked_count'].median(), df[1]['all_count'].median()))

    print('#### Mean ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(df[1]['tracking_count'].mean(), df[1]['linked_count'].mean(), df[1]['unlinked_count'].mean(), df[1]['all_count'].mean()))

    print('#### SD ####')
    print("Tracking: {}, Linked: {}, Unlinked: {}, Total: {}".format(df[1]['tracking_count'].std(), df[1]['linked_count'].std(), df[1]['unlinked_count'].std(), df[1]['all_count'].std()))

# %% Percentage of apps using tracking, linked, unlinked data

for df in apps: 
    t_percentage = sum(df[1]['has_tracking']) / len(df[1]) * 100
    l_percentage = sum(df[1]['has_linked']) / len(df[1]) * 100
    u_percentage = sum(df[1]['has_unlinked']) / len(df[1]) * 100
    any_percentage = sum(df[1]['has_any']) / len(df[1]) * 100

    print("In the {} apps there are {}% using tracking data, {}% using linked data, and {}% using unlinked data, and {}% using data of any kind".format(df[0], round(t_percentage,2), round(l_percentage,2), round(u_percentage,2), round(any_percentage,2) ))

# %%
