# %% Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from minisom import MiniSom

# %% Load raw data files

apps = pd.read_csv('../data/processed/apps_top1000_all.csv', delimiter=';') 

# %% Helper vars

data_types = ['Health & Fitness', 'Location', 'Contact Info', 'Diagnostics', 'Sensitive Info', 'Usage Data', 'Browsing History', 'Contacts', 'Purchases', 'Identifiers', 'Other Data', 'Financial Info', 'Search History', 'User Content']

purposes = ['App Functionality', 'Other Purposes', 'Analytics', 'Developers Advertising', 'Product Personalization', 'Third Party Advertising']

tracking_colnames = ['t' + x.replace(' ', '') for x in data_types]
linked_colnames = ['l' + x.replace(' ', '') for x in data_types]
unlinked_colnames = ['u' + x.replace(' ', '') for x in data_types]

input_data = apps[tracking_colnames + linked_colnames + unlinked_colnames]

# %% Try to SOM

import pandas as pd
import numpy as np
columns=['area', 'perimeter', 'compactness', 'length_kernel', 'width_kernel',
                   'asymmetry_coefficient', 'length_kernel_groove', 'target']
data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt', 
                    names=columns, 
                   sep='\t+', engine='python')
target = data['target'].values
label_names = {1:'Kama', 2:'Rosa', 3:'Canadian'}
data = data[data.columns[:-1]]
# data normalization
data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
data = data.values

# Initialization and training
n_neurons = 9
m_neurons = 9
som = MiniSom(n_neurons, m_neurons, data.shape[1], sigma=1.5, learning_rate=.5, 
              neighborhood_function='gaussian', random_seed=0)

som.pca_weights_init(data)
som.train(data, 1000, verbose=True)

# Show resuts
plt.figure(figsize=(9, 9))

plt.pcolor(som.distance_map().T, cmap='bone_r')  # plotting the distance map as background
plt.colorbar()

# Plotting the response for each pattern in the iris dataset
# different colors and markers for each label
markers = ['o', 's', 'D']
colors = ['C0', 'C1', 'C2']
for cnt, xx in enumerate(data):
    w = som.winner(xx)  # getting the winner
    # palce a marker on the winning position for the sample xx
    plt.plot(w[0]+.5, w[1]+.5, markers[target[cnt]-1], markerfacecolor='None',
             markeredgecolor=colors[target[cnt]-1], markersize=12, markeredgewidth=2)

plt.show()

# %%
