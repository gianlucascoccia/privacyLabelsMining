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

# %% Usages by category

usages = apps.groupby(['category']).size().reset_index(name = 'app_count')
usages['tracking_count'] = apps[apps['has_tracking']].groupby(['category']).size().values
usages['linked_count'] = apps[apps['has_linked']].groupby(['category']).size().values
usages['unlinked_count'] = apps[apps['has_unlinked']].groupby(['category']).size().values
usages['tracking_percentage'] = usages['tracking_count'] / usages['app_count'] * 100
usages['linked_percentage'] = usages['linked_count'] / usages['app_count'] * 100
usages['unlinked_percentage'] = usages['unlinked_count'] / usages['app_count'] * 100

usages = usages.sort_values(by='tracking_percentage', ascending=True)
usages.reset_index(drop=True, inplace=True)

# %% Bar plot by category

barWidth = 0.33

fig = plt.figure(num=None, figsize=(4.5, 8), dpi=80, facecolor='w', edgecolor='k')

plt.xlim(0,110)
plt.ylim(-1.75, len(usages) * 1.33)

# Set position of bar on y axis
r1 = np.arange(len(usages))
r2 = [x * 1.33 for x in r1]
r1 = [x - barWidth for x in r2]
r3 = [x + barWidth for x in r2]

plt.barh(r3, usages.tracking_percentage, color='red', height=barWidth, label='Tracking data')
plt.barh(r2, usages.linked_percentage, color='blue', height=barWidth, label='Linked data')
plt.barh(r1, usages.unlinked_percentage, color='green', height=barWidth, label='Unlinked data')

plot_ticks = [x.replace('&', ' & ').capitalize() for x in usages.category]

# Add xticks on the middle of the group bars
plt.ylabel('App category', size=8)
plt.xlabel('Usages % (#)', size=8)
plt.yticks(r2, plot_ticks, size=7)
plt.xticks(size=7) 

# Add text on bars
textsize = 4.5
def format_label(percentage, count):
    return '{}% ({})'.format(round(percentage,2), count)

for index, row in usages.iterrows():
    plt.text(row['tracking_percentage'] + 1, r3[index] - 0.1, format_label(row['tracking_percentage'], row['tracking_count']), size = textsize)
    plt.text(row['linked_percentage'] + 1, r2[index] - 0.1, format_label(row['linked_percentage'], row['linked_count']), size = textsize)
    plt.text(row['unlinked_percentage'] + 1, r1[index] - 0.1, format_label(row['unlinked_percentage'], row['unlinked_count']), size = textsize)
    
plt.legend(fontsize=5.5, loc="lower left", ncol=3)
plt.tight_layout()
plt.savefig('figures/Usages.pdf', dpi=300)  
plt.show()

# %%
