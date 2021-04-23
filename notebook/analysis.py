# %% Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Purposes by data type
purposes_linked_colnames = []
for x in purposes:
    purposes_linked_colnames.extend(['l' + x.replace(' ', '') + y.replace(' ', '') for y in data_types]) 

purposes_unlinked_colnames = []
for x in purposes:
    purposes_unlinked_colnames.extend(['u' + x.replace(' ', '') + y.replace(' ', '') for y in data_types]) 

purposes_tracking_colnames = []
for x in purposes:
    purposes_tracking_colnames.extend(['t' + x.replace(' ', '') + y.replace(' ', '') for y in data_types]) 

# %% Infer purpose of tracking data 

# Example
#apps['tThirdPartyAdvertisingContactInfo'] = ((apps['uThirdPartyAdvertisingContactInfo'] + apps['lThirdPartyAdvertisingContactInfo']) >= 1) & (apps['tContactInfo'] >= 1)

for dt in data_types:
    for p in purposes:
        curr = p.replace(' ', '') + dt.replace(' ', '')
        apps['t' + curr] = ((apps['u' + curr] + apps['l' + curr]) >= 1) & (apps['t' + dt.replace(' ','')] >= 1)

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

# %% Flags of types of purposes

apps['has_app_functionality'] = apps['app_functionality_count'].apply(lambda x: x > 0)
apps['has_analytics'] = apps['analytics_count'].apply(lambda x: x > 0)
apps['has_developers_advertising'] = apps['developers_advertising_count'].apply(lambda x: x > 0)
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
    print('---------------- {} -----------------'.format(df[0]))

    # App functionality
    af_t_percentage = sum([x > 0 for x in df[1][app_functionality_tracking_colnames].sum(axis=1)]) / len(df[1]) * 100
    af_l_percentage = sum([x > 0 for x in df[1][app_functionality_linked_colnames].sum(axis=1)]) / len(df[1]) * 100
    af_u_percentage = sum([x > 0 for x in df[1][app_functionality_unlinked_colnames].sum(axis=1)]) / len(df[1]) * 100
    af_percentage = sum(df[1]['has_app_functionality']) / len(df[1]) * 100

    print("App functionality: Tracking {}, Linked {}, Unlinked {}, Any: {}".format(round(af_t_percentage,2), round(af_l_percentage,2), round(af_u_percentage,2), round(af_percentage,2)))

    # Analytics
    an_t_percentage = sum([x > 0 for x in df[1][analytics_tracking_colnames].sum(axis=1)]) / len(df[1]) * 100
    an_l_percentage = sum([x > 0 for x in df[1][analytics_linked_colnames].sum(axis=1)]) / len(df[1]) * 100
    an_u_percentage = sum([x > 0 for x in df[1][analytics_unlinked_colnames].sum(axis=1)]) / len(df[1]) * 100
    an_percentage = sum(df[1]['has_analytics']) / len(df[1]) * 100

    print("Analytics: Tracking {}, Linked {}, Unlinked {}, Any: {}".format(round(an_t_percentage,2), round(an_l_percentage,2), round(an_u_percentage,2), round(an_percentage,2)))

    # Product personalization
    pp_t_percentage = sum([x > 0 for x in df[1][product_personalization_tracking_colnames].sum(axis=1)]) / len(df[1]) * 100
    pp_l_percentage = sum([x > 0 for x in df[1][product_personalization_linked_colnames].sum(axis=1)]) / len(df[1]) * 100
    pp_u_percentage = sum([x > 0 for x in df[1][product_personalization_unlinked_colnames].sum(axis=1)]) / len(df[1]) * 100
    pp_percentage = sum(df[1]['has_product_personalization']) / len(df[1]) * 100

    print("Product personalization: Tracking {}, Linked {}, Unlinked {}, Any: {}".format(round(pp_t_percentage,2), round(pp_l_percentage,2), round(pp_u_percentage,2), round(pp_percentage,2)))

    # Other purposes
    op_t_percentage = sum([x > 0 for x in df[1][other_purposes_tracking_colnames].sum(axis=1)]) / len(df[1]) * 100
    op_l_percentage = sum([x > 0 for x in df[1][other_purposes_linked_colnames].sum(axis=1)]) / len(df[1]) * 100
    op_u_percentage = sum([x > 0 for x in df[1][other_purposes_unlinked_colnames].sum(axis=1)]) / len(df[1]) * 100
    op_percentage = sum(df[1]['has_other_purposes']) / len(df[1]) * 100

    print("Other purposes: Tracking {}, Linked {}, Unlinked {}, Any: {}".format(round(op_t_percentage,2), round(op_l_percentage,2), round(op_u_percentage,2), round(op_percentage,2)))

    # Developers advertising
    da_t_percentage = sum([x > 0 for x in df[1][developers_advertising_tracking_colnames].sum(axis=1)]) / len(df[1]) * 100
    da_l_percentage = sum([x > 0 for x in df[1][developers_advertising_linked_colnames].sum(axis=1)]) / len(df[1]) * 100
    da_u_percentage = sum([x > 0 for x in df[1][developers_advertising_unlinked_colnames].sum(axis=1)]) / len(df[1]) * 100
    da_percentage = sum(df[1]['has_developers_advertising']) / len(df[1]) * 100

    print("Developer advertising: Tracking {}, Linked {}, Unlinked {}, Any: {}".format(round(da_t_percentage,2), round(da_l_percentage,2), round(da_u_percentage,2), round(da_percentage,2)))
    
    # Third party advertising
    tpa_t_percentage = sum([x > 0 for x in df[1][third_party_advertising_tracking_colnames].sum(axis=1)]) / len(df[1]) * 100
    tpa_l_percentage = sum([x > 0 for x in df[1][third_party_advertising_linked_colnames].sum(axis=1)]) / len(df[1]) * 100
    tpa_u_percentage = sum([x > 0 for x in df[1][third_party_advertising_unlinked_colnames].sum(axis=1)]) / len(df[1]) * 100
    tpa_percentage = sum(df[1]['has_third_party_advertising']) / len(df[1]) * 100
    
    print("3rd party advertising: Tracking {}, Linked {}, Unlinked {}, Any: {}".format(round(tpa_t_percentage,2), round(tpa_l_percentage,2), round(tpa_u_percentage,2), round(tpa_percentage,2)))

# %% For each purpose, how much tracking data is used?

#TODO: Check this part!!!

for df in apps_types: 
    print('---------------- {} -----------------'.format(df[0]))

    for p in purposes:
        print(p)
        tracking_cols_purpose = ['t' + p.replace(' ','') + d.replace(' ','') for d in data_types]
        tracking_cols_purpose_count = sum(
        [x > 0 for x in df[1][tracking_cols_purpose].sum(axis=1)])
         
        purpose_tracking_percentage = tracking_cols_purpose_count / sum(df[1]['has_' + p.lower().replace(' ', '_')]) * 100
        
        print(round(purpose_tracking_percentage,2))


# %% Correlations

# TODO: automate the analysis of results

apps.corr(method='spearman').to_csv('correlation.csv')

# %% Plot ranking vs data used

plot_data = apps
plot_data.dropna(subset=['top_chart_position_free'])

fig = plt.figure(figsize=(15, 8))
plt.scatter(plot_data['tracking_count'], plot_data['top_chart_position_free']) 
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('figures/tracking_vs_ranking.png', facecolor='white')


# %%
