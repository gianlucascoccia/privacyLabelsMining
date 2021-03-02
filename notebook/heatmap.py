# %% Imports

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

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

labels = labels.drop(columns=['category'])

tLabels = labels[tracking_colnames]
lLabels = labels[linked_colnames]
uLabels = labels[unlinked_colnames]

tTotals = tLabels.sum()
lTotals = lLabels.sum()
uTotals = uLabels.sum()

labels = labels
tLabels = tLabels.values
lLabels = lLabels.values
uLabels = uLabels.values

sumLabel = ['Sum total']

# %% Create plot

grid_rows = len(categories) + 1
grid_cols = len(data_types) * 3

fig = plt.figure(figsize=(20,10))

# Top subplots
ax_t = plt.subplot2grid((grid_rows,grid_cols), (0,0), rowspan=len(categories), colspan=len(data_types))
ax_l = plt.subplot2grid((grid_rows,grid_cols), (0,len(data_types)), rowspan=len(categories), colspan=len(data_types))
ax_u = plt.subplot2grid((grid_rows,grid_cols), (0,2 * len(data_types)), rowspan=len(categories), colspan=len(data_types))

# Bottom subplots
ax_tc = plt.subplot2grid((grid_rows,grid_cols), (len(categories), 0), rowspan=1, colspan=len(data_types))
ax_lc = plt.subplot2grid((grid_rows,grid_cols), (len(categories), len(data_types)), rowspan=1, colspan=len(data_types))
ax_uc = plt.subplot2grid((grid_rows,grid_cols), (len(categories), 2*len(data_types)), rowspan=1, colspan=len(data_types))

# Create top heatmaps
im_t = ax_t.imshow(tLabels, cmap='OrRd', aspect='auto') 
im_l = ax_l.imshow(lLabels, cmap='OrRd', aspect='auto')
im_u = ax_u.imshow(uLabels, cmap='OrRd', aspect='auto')

# Create bottom heatmaps
im_tc = ax_tc.imshow(np.array(tTotals.values.reshape(1,len(tTotals))), cmap='OrRd', aspect='auto')
im_lc = ax_lc.imshow(np.array(lTotals.values.reshape(1,len(lTotals))), cmap='OrRd', aspect='auto')
im_uc = ax_uc.imshow(np.array(uTotals.values.reshape(1,len(uTotals))), cmap='OrRd', aspect='auto')

# Show ticks
ax_t.set_xticks([])
ax_l.set_xticks([])
ax_u.set_xticks([])

ax_tc.set_xticks(np.arange(len(data_types)))
ax_lc.set_xticks(np.arange(len(data_types)))
ax_uc.set_xticks(np.arange(len(data_types)))

ax_t.set_yticks(np.arange(len(categories)))
ax_l.set_yticks([])
ax_u.set_yticks([])

ax_tc.set_yticks(np.arange(len(sumLabel)))
ax_lc.set_yticks([])
ax_uc.set_yticks([])

# Label ticks 
ax_tc.set_xticklabels(data_types)
ax_lc.set_xticklabels(data_types)
ax_uc.set_xticklabels(data_types)

plt.setp(ax_tc.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
plt.setp(ax_lc.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
plt.setp(ax_uc.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

ax_t.set_yticklabels(categories)
ax_tc.set_yticklabels(sumLabel)

# Plot titles
ax_t.title.set_text('Tracking')
ax_l.title.set_text('Linked')
ax_u.title.set_text('Unlinked')

# Loop over data dimensions and create text annotations.
for i in range(len(categories)):
    for j in range(len(data_types)):
        ax_t.text(j, i, int(tLabels[i, j]), ha="center", va="center")
        ax_l.text(j, i, int(lLabels[i, j]), ha="center", va="center")
        ax_u.text(j, i, int(uLabels[i, j]), ha="center", va="center")

for i in range(len(data_types)):
    ax_tc.text(i,0, int(tTotals[i]), ha="center", va="center")
    ax_lc.text(i,0, int(lTotals[i]), ha="center", va="center")
    ax_uc.text(i,0, int(uTotals[i]), ha="center", va="center")

plt.savefig('figures/labels_heatmap.png')

# %%
