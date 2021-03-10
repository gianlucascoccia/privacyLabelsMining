# %% Imports

import csv
import glob
import unicodedata
import os.path as path
from bs4 import BeautifulSoup

# %% Load html files

filesFolder = "../data/raw/appMagicHTML/top1000/top_grossing"
html_files = glob.glob(path.join(filesFolder, "*.htm"))

# %% Set up output file

OUT_FILE = "../data/raw/top_1000_apps_top_grossing.csv"

out_file = open(OUT_FILE, 'w')
writer = csv.DictWriter(out_file, fieldnames=['id', 'top_chart_position','category','name','publisher'], delimiter=";", quoting=csv.QUOTE_MINIMAL) 
writer.writeheader()

# %% parse files

for f in html_files:
    # read file
    soup = BeautifulSoup(open(f).read())

    # extract file name (AKA category name)
    category = path.basename(f).split(".")[0]
    
    # get html list
    app_list = soup.find('top-apps-col')
    apps = app_list.findAll('app-list-item')

    # parse list
    parsed_app = {}
    for app in apps:

        # get app chart position
        app_position = int(app.find("div", {"class": "top-position-number"}).text)

        # get app name
        name = unicodedata.normalize("NFKD",str(app.find("a", {"class": "app-name"}).text))

        # get app publisher
        publisher = unicodedata.normalize("NFKD",str(app.find("a", {"app-publisher-name"}).text))

        # get app store id
        store_id = app.find("a", {"class": "app-name"})['href'].split('/')[3]
        
        # update results
        parsed_app.update({
            'id': store_id,
            'top_chart_position': app_position,
            'category': category,
            'name': name,
            'publisher': publisher
        })

        writer.writerow(parsed_app)

# %%
