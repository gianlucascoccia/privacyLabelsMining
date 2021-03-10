# %% Imports

import csv
import os.path as path
import requests

# %% Script params

IN_FILE = "../data/raw/top_1000_apps_free_store_data.csv"
outFolder = "../data/raw/storePageHTML"

# %% download and save the store page for each app

# Open app list
reader = csv.DictReader(open(IN_FILE, 'r'), delimiter=";")

for index, a in enumerate(reader):
    print("Processing app {}, id {} on row {}".format(a['title'], a['id'], index))
    
    if a['url'] == 'NA':
        continue
    
    out_file_path = path.join(outFolder, a['id'] + '.htm')

    if path.isfile(out_file_path):
        continue
    
    r = requests.get(a['url'])
    if r.status_code == 200:        
        with open(out_file_path, 'wb') as out_file:
            out_file.write(r.content)
    else:
        print("An error as occurred for url {}".format(a['url']))
    
# %%
