# %% Imports

import csv
import os.path as path
import requests

# %% Script params

OUT_FILE = "../data/raw/apps_store_data.csv"
outFolder = "../data/raw/storePageHTML"

# %% download and save the store page for each app

# Open app list
reader = csv.DictReader(open(OUT_FILE, 'r'), delimiter=";")

for index, a in enumerate(reader):
    print("Processing app {}, id {} on row {}".format(a['title'], a['id'], index))
    if a['url'] == 'NA':
        continue
    r = requests.get(a['url'])
    if r.status_code == 200:    
        out_file_path = path.join(outFolder, a['id'] + '.htm')
        with open(out_file_path, 'wb') as out_file:
            out_file.write(r.content)
    else:
        print("An error as occurred for url {}".format['a.url'])
    
# %%
