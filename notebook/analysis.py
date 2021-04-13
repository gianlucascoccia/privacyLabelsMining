# %% Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% Load raw data files

apps = pd.read_csv('../data/processed/apps_top1000_all.csv', delimiter=';') 

# %% Helper vars

data_types = ['Health & Fitness', 'Location', 'Contact Info', 'Diagnostics', 'Sensitive Info', 'Usage Data', 'Browsing History', 'Contacts', 'Purchases', 'Identifiers', 'Other Data', 'Financial Info', 'Search History', 'User Content']

purposes = ['App functionality', 'Other purposes', 'Analytics', 'Developers advertising', 'Product personalization', 'Third party advertising']

tracking_colnames = ['t' + x.replace(' ', '') for x in data_types]
linked_colnames = ['l' + x.replace(' ', '') for x in data_types]
unlinked_colnames = ['u' + x.replace(' ', '') for x in data_types]

app_functionality_colnames = [p + x for p in ['l', 'u'] for x in ['app_functionality' + '_' + d.replace(' ','_').lower() for d in data_types]]
other_purposes_colnames = [p + x for p in ['l', 'u'] for x in ['other_purposes' + '_' + d.replace(' ','_').lower() for d in data_types]]
analytics_colnames = [p + x for p in ['l', 'u'] for x in ['analytics' + '_' + d.replace(' ','_').lower() for d in data_types]]
developer_advertising_colnames = [p + x for p in ['l', 'u'] for x in ['developers_advertising' + '_' + d.replace(' ','_').lower() for d in data_types]]
product_personalization_colnames = [p + x for p in ['l', 'u'] for x in ['product_personalization' + '_' + d.replace(' ','_').lower() for d in data_types]]
third_party_advertising_colnames = [p + x for p in ['l', 'u'] for x in ['third_party_advertising' + '_' + d.replace(' ','_').lower() for d in data_types]]

purposes_linked_colnames = []
for x in purposes:
    purposes_linked_colnames.extend(['l' + x.replace(' ', '_').lower() + '_' + y.lower() for y in data_types]) 

purposes_unlinked_colnames = []
for x in purposes:
    purposes_unlinked_colnames.extend(['u' + x.replace(' ', '_').lower() + '_' + y.lower() for y in data_types]) 

# %% Counts of tracking, linked and unlinked

apps['tracking_count'] = apps[tracking_colnames].sum(axis=1)
apps['linked_count'] = apps[linked_colnames].sum(axis=1)
apps['unlinked_count'] = apps[unlinked_colnames].sum(axis=1)
apps['all_count'] = apps['tracking_count'] + apps['linked_count'] + apps['unlinked_count']

# %% Counts of purposes 
 
apps['app_functionality_count'] = apps[app_functionality_colnames].sum(axis=1)
apps['analytics_count'] = apps[analytics_colnames].sum(axis=1)
apps['developer_advertising_count'] = apps[developer_advertising_colnames].sum(axis=1)
apps['third_party_advertising_count'] = apps[third_party_advertising_colnames].sum(axis=1)
apps['other_purposes_count'] = apps[other_purposes_colnames].sum(axis=1)
apps['product_personalization_count'] = apps[product_personalization_colnames].sum(axis=1)

# %% Flags of types of data usage

apps['has_tracking'] = apps['tracking_count'].apply(lambda x: x > 0)
apps['has_linked'] = apps['linked_count'].apply(lambda x: x > 0)        
apps['has_unlinked'] = apps['unlinked_count'].apply(lambda x: x > 0)
apps['has_any'] = apps['all_count'].apply(lambda x: x > 0)        

# %% Flags of types of purposes

apps['has_app_functionality'] = apps['app_functionality_count'].apply(lambda x: x > 0)
apps['has_analytics'] = apps['analytics_count'].apply(lambda x: x > 0)
apps['has_developer_advertising'] = apps['developer_advertising_count'].apply(lambda x: x > 0)
apps['has_third_party_advertising'] = apps['third_party_advertising_count'].apply(lambda x: x > 0)
apps['has_other_purposes'] = apps['other_purposes_count'].apply(lambda x: x > 0)
apps['has_product_personalization'] = apps['product_personalization_count'].apply(lambda x: x > 0)

# %% Divide in free and paid

apps_free = apps[apps['free'] == True] 
apps_paid = apps[apps['free'] == False] 

apps_types = [('free', apps_free), ('paid', apps_paid)]

# %% Summary stats for tracking, linked, unlinked

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

# %% Percentage of apps employing data for each purpose

for df in apps_types: 
    print("{} {} apps".format(df[0], len(df[1])))

for df in apps_types: 
    af_percentage = sum(df[1]['has_app_functionality']) / len(df[1]) * 100
    an_percentage = sum(df[1]['has_analytics']) / len(df[1]) * 100
    pp_percentage = sum(df[1]['has_product_personalization']) / len(df[1]) * 100
    op_percentage = sum(df[1]['has_other_purposes']) / len(df[1]) * 100
    da_percentage = sum(df[1]['has_developer_advertising']) / len(df[1]) * 100
    tpa_percentage = sum(df[1]['has_third_party_advertising']) / len(df[1]) * 100
    
    print("In the {} apps there are: \n {}% using data for app functionality \n {}% using data for analytics \n {}% using data for product personalization \n {}% using data for other purposes \n {}% using data for developer advertising \n {}% using data for 3rd party advertising".format(df[0], round(af_percentage,2), round(an_percentage,2), round(pp_percentage,2), round(op_percentage,2), round(da_percentage,2), round(tpa_percentage,2)))


# %% Correlations
apps.corr(method='spearman').to_csv('correlation.csv')

# %%
