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

tracking_colnames = ['t' + x.replace(' ', '') for x in data_types]
linked_colnames = ['l' + x.replace(' ', '') for x in data_types]
unlinked_colnames = ['u' + x.replace(' ', '') for x in data_types]

input_data = apps[tracking_colnames + linked_colnames + unlinked_colnames]

# %% Counts of tracking, linked and unlinked

apps['tracking_count'] = apps[tracking_colnames].sum(axis=1)
apps['linked_count'] = apps[linked_colnames].sum(axis=1)
apps['unlinked_count'] = apps[unlinked_colnames].sum(axis=1)
apps['all_count'] = apps['tracking_count'] + apps['linked_count'] + apps['unlinked_count']

# %% Perform t-sne

tsne = manifold.TSNE(n_components=2,  init='pca', perplexity=50, random_state=0)
t0 = time()
output = tsne.fit_transform(input_data)
t1 = time()
print("Took {} sec".format(t1-t0))

# %% Visualize results


#apps['publisher_ID'] = apps.publisher.astype('category').cat.rename_categories(range(1, apps.publisher.nunique()+1))

apps['category_ID'] = apps.category.astype('category').cat.rename_categories(range(1, apps.category.nunique()+1))

#apps['free_ID'] = apps.free.astype('category').cat.rename_categories(range(1, apps.free.nunique()+1))

fig = plt.figure(figsize=(15, 8))
plt.scatter(output[:, 0], output[:, 1], c=apps['category_ID'], cmap=plt.cm.Set1) 
plt.savefig('figures/t-sne-number.png', facecolor='white')
plt.show()

# %%
