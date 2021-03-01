# %% Imports

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# %% Load raw data files

apps = pd.read_csv('../data/processed/apps.csv', delimiter=';') 

# %% Helper vars

data_types = ['Health & Fitness', 'Location', 'Contact Info', 'Diagnostics', 'Sensitive Info', 'Usage Data', 'Browsing History', 'Contacts', 'Purchases', 'Identifiers', 'Other Data', 'Financial Info', 'Search History', 'User Content']

categories = [x.replace('&',' & ').title() for x in np.unique(apps['category'])]

tracking_colnames = ['t' + x.replace(' ', '') for x in data_types]
linked_colnames = ['l' + x.replace(' ', '') for x in data_types]
unlinked_colnames = ['u' + x.replace(' ', '') for x in data_types]
all_colnames = tracking_colnames + linked_colnames + unlinked_colnames

label_cols = apps[['category'] + tracking_colnames + linked_colnames + unlinked_colnames] 

labels = label_cols.groupby('category').sum().reset_index()

totals = label_cols.sum()

labels = labels.drop(columns=['category'])

tLabels = labels[tracking_colnames]
lLabels = labels[linked_colnames]
uLabels = labels[unlinked_colnames]

labels = labels
tLabels = tLabels.values
lLabels = lLabels.values
uLabels = uLabels.values

# %% Create plot

fig, axes = plt.subplots(ncols=3, figsize=(20, 10))

ax_t, ax_l, ax_u = axes

im_t = ax_t.imshow(tLabels, cmap='YlGn') #Oranges
im_l = ax_l.imshow(lLabels, cmap='YlGn')
im_u = ax_u.imshow(uLabels, cmap='YlGn')

# Show all ticks
ax_t.set_xticks(np.arange(len(data_types)))
ax_l.set_xticks(np.arange(len(data_types)))
ax_u.set_xticks(np.arange(len(data_types)))

ax_t.set_yticks(np.arange(len(categories)))
ax_l.set_yticks([])
ax_u.set_yticks([])

# Label ticks 
ax_t.set_xticklabels(data_types)
ax_l.set_xticklabels(data_types)
ax_u.set_xticklabels(data_types)

plt.setp(ax_t.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
plt.setp(ax_l.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
plt.setp(ax_u.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

ax_t.set_yticklabels(categories)

# Loop over data dimensions and create text annotations.
for i in range(len(categories)):
    for j in range(len(data_types)):
        ax_t.text(j, i, int(tLabels[i, j]), ha="center", va="center")
        ax_l.text(j, i, int(lLabels[i, j]), ha="center", va="center")
        ax_u.text(j, i, int(uLabels[i, j]), ha="center", va="center")

fig.tight_layout()
plt.savefig('figures/labels_heatmap.png')

# %%
