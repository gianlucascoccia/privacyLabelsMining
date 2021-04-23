# %% Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import manifold
from time import time

# %% Load raw data files

apps = pd.read_csv('../data/processed/apps_top1000_all.csv', delimiter=';') 

# %% Helper vars
data_types = ['Health & Fitness', 'Location', 'Contact Info', 'Diagnostics', 'Sensitive Info', 'Usage Data', 'Browsing History', 'Contacts', 'Purchases', 'Identifiers', 'Other Data', 'Financial Info', 'Search History', 'User Content']

purposes = ['App Functionality', 'Other Purposes', 'Analytics', 'Developers Advertising', 'Product Personalization', 'Third Party Advertising']

# Type of data
tracking_colnames = ['t' + x.replace(' ', '') for x in data_types]
linked_colnames = ['l' + x.replace(' ', '') for x in data_types]
unlinked_colnames = ['u' + x.replace(' ', '') for x in data_types]

# Purposes - App functionality
app_functionality_tracking_colnames = ['tAppFunctionality' + d.replace(' ','') for d in data_types]
app_functionality_linked_colnames = ['lAppFunctionality' + d.replace(' ','') for d in data_types]
app_functionality_unlinked_colnames = ['uAppFunctionality' + d.replace(' ','') for d in data_types]
app_functionality_colnames = app_functionality_tracking_colnames + app_functionality_linked_colnames + app_functionality_unlinked_colnames

# Purposes - Other purposes
other_purposes_tracking_colnames = ['tOtherPurposes' + d.replace(' ','') for d in data_types]
other_purposes_linked_colnames = ['lOtherPurposes' + d.replace(' ','') for d in data_types]
other_purposes_unlinked_colnames = ['uOtherPurposes' + d.replace(' ','') for d in data_types]
other_purposes_colnames = other_purposes_tracking_colnames + other_purposes_linked_colnames + other_purposes_unlinked_colnames

# Purposes - Analytics 
analytics_tracking_colnames = ['tAnalytics' + d.replace(' ','') for d in data_types]
analytics_linked_colnames = ['lAnalytics' + d.replace(' ','') for d in data_types]
analytics_unlinked_colnames = ['uAnalytics' + d.replace(' ','') for d in data_types]
analytics_colnames = analytics_tracking_colnames + analytics_linked_colnames + analytics_unlinked_colnames

# Purposes - Developers advertising 
developers_advertising_tracking_colnames = ['tDevelopersAdvertising' + d.replace(' ','') for d in data_types]
developers_advertising_linked_colnames = ['lDevelopersAdvertising' + d.replace(' ','') for d in data_types]
developers_advertising_unlinked_colnames = ['uDevelopersAdvertising' + d.replace(' ','') for d in data_types]
developers_advertising_colnames = developers_advertising_tracking_colnames + developers_advertising_linked_colnames + developers_advertising_unlinked_colnames

# Purposes - Product personalization
product_personalization_tracking_colnames = ['tProductPersonalization' + d.replace(' ','') for d in data_types]
product_personalization_linked_colnames = ['lProductPersonalization' + d.replace(' ','') for d in data_types]
product_personalization_unlinked_colnames = ['uProductPersonalization' + d.replace(' ','') for d in data_types]
product_personalization_colnames = product_personalization_tracking_colnames + product_personalization_linked_colnames + product_personalization_unlinked_colnames

# Purposes - Third party advertising
third_party_advertising_tracking_colnames =['tThirdPartyAdvertising' + d.replace(' ','') for d in data_types]
third_party_advertising_linked_colnames = ['lThirdPartyAdvertising' + d.replace(' ','') for d in data_types]
third_party_advertising_unlinked_colnames = ['uThirdPartyAdvertising' + d.replace(' ','') for d in data_types]
third_party_advertising_colnames = third_party_advertising_tracking_colnames + third_party_advertising_linked_colnames + third_party_advertising_unlinked_colnames

# %% Infer purpose of tracking data 

# Example
#apps['tThirdPartyAdvertisingContactInfo'] = ((apps['uThirdPartyAdvertisingContactInfo'] + apps['lThirdPartyAdvertisingContactInfo']) >= 1) & (apps['tContactInfo'] >= 1)

for dt in data_types:
    for p in purposes:
        curr = p.replace(' ', '') + dt.replace(' ', '')
        apps['t' + curr] = ((apps['u' + curr] + apps['l' + curr]) >= 1) & (apps['t' + dt.replace(' ','')] >= 1)

# %% Select data for tsne        

purposes_colnames = app_functionality_unlinked_colnames + other_purposes_colnames + product_personalization_colnames + developers_advertising_colnames + third_party_advertising_colnames + analytics_colnames
input_data = apps[tracking_colnames + linked_colnames + unlinked_colnames + purposes_colnames]

# %% Counts of tracking, linked and unlinked

apps['tracking_count'] = apps[tracking_colnames].sum(axis=1)
apps['linked_count'] = apps[linked_colnames].sum(axis=1)
apps['unlinked_count'] = apps[unlinked_colnames].sum(axis=1)
apps['all_count'] = apps['tracking_count'] + apps['linked_count'] + apps['unlinked_count']

# %% Counts of purposes 
 
apps['app_functionality_count'] = apps[app_functionality_linked_colnames + app_functionality_unlinked_colnames].sum(axis=1)
apps['analytics_count'] = apps[analytics_linked_colnames + analytics_unlinked_colnames].sum(axis=1)
apps['developers_advertising_count'] = apps[developers_advertising_linked_colnames + developers_advertising_unlinked_colnames].sum(axis=1)
apps['third_party_advertising_count'] = apps[third_party_advertising_linked_colnames + third_party_advertising_unlinked_colnames].sum(axis=1)
apps['other_purposes_count'] = apps[other_purposes_linked_colnames + other_purposes_unlinked_colnames].sum(axis=1)
apps['product_personalization_count'] = apps[product_personalization_linked_colnames + product_personalization_unlinked_colnames].sum(axis=1)

# %% Flags of types of data usage

apps['has_tracking'] = apps['tracking_count'].apply(lambda x: x > 0)
apps['has_linked'] = apps['linked_count'].apply(lambda x: x > 0)        
apps['has_unlinked'] = apps['unlinked_count'].apply(lambda x: x > 0)
apps['has_any'] = apps['all_count'].apply(lambda x: x > 0)  
apps['no_linked'] = (apps['linked_count'] == 0) & (apps['unlinked_count'] > 0) 
apps['no_linked_no_tracking'] = apps['no_linked'] & (apps['tracking_count'] == 0)


# %% Flags of types of purposes

apps['has_app_functionality'] = apps['app_functionality_count'].apply(lambda x: x > 0)
apps['has_analytics'] = apps['analytics_count'].apply(lambda x: x > 0)
apps['has_developers_advertising'] = apps['developers_advertising_count'].apply(lambda x: x > 0)
apps['has_third_party_advertising'] = apps['third_party_advertising_count'].apply(lambda x: x > 0)
apps['has_other_purposes'] = apps['other_purposes_count'].apply(lambda x: x > 0)
apps['has_product_personalization'] = apps['product_personalization_count'].apply(lambda x: x > 0)

# %% Can't perform T-SNE with nan values

apps = apps.dropna(subset=tracking_colnames + linked_colnames + unlinked_colnames + purposes_colnames)

# %% Perform t-sne

tsne = manifold.TSNE(n_components=2,  init='pca', perplexity=50, random_state=0)
t0 = time()
output = tsne.fit_transform(input_data.dropna())
t1 = time()
print("Took {} sec".format(t1-t0))

# %% Visualize results

## LOOP CODE

#colnames = ['t' + x.replace(' ','') for x in data_types]
colnames = [x.lower().replace(' ','_') for x in purposes]
#colnames = third_party_advertising_tracking_colnames + product_personalization_tracking_colnames + developers_advertising_tracking_colnames + analytics_tracking_colnames + other_purposes_tracking_colnames + app_functionality_tracking_colnames

for colname in colnames:

    #apps['has_' + colname] = apps[colname] > 0

    fig = plt.figure(figsize=(15, 8))
    plt.scatter(output[:, 0], output[:, 1], c=~(apps['has_' + colname]).astype(bool), cmap=plt.cm.Set1) 
    plt.tight_layout()
    plt.savefig('figures/t-sne/{}.png'.format(colname), facecolor='white')
    plt.show()


## Single figure code

#apps['category_ID'] = apps.category.astype('category').cat.rename_categories(range(1, apps.category.nunique()+1))

#apps['only_unlinked_ID'] = apps.only_unlinked.astype('category').cat.rename_categories(range(1, apps.free.nunique()+1))

#fig = plt.figure(figsize=(15, 8))
#plt.scatter(output[:, 0], output[:, 1], c=~(apps['no_linked_no_tracking']).astype(bool), cmap=plt.cm.Set1) 
#plt.tight_layout()
#plt.savefig('figures/t-sne/no_linked_no_tracking.png', facecolor='white')
#plt.show()


# %%
