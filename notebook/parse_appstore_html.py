# %% Imports

import csv
import glob
import os.path as path
from bs4 import BeautifulSoup

# %% Script parameters

# List of apps for which parse data
APP_LIST = "../data/raw/top_apps_list.csv"

# Folder with raw html app store pages
HTMLfilesFolder = "../data/raw/storePageHTML"

# File to save output
OUT_FILE = "../data/raw/privacy_labels.csv"

data_types = ['Health & Fitness', 'Location', 'Contact Info', 'Diagnostics', 'Sensitive Info', 'Usage Data', 'Browsing History', 'Contacts', 'Purchases', 'Identifiers', 'Other Data', 'Financial Info', 'Search History', 'User Content']

names_map = {
    'Data Used to Track You':'t',
    'Data Linked to You':'l',
    'Data Not Linked to You':'u',
}

# %% open output file
labels_list = csv.DictWriter(open(OUT_FILE, 'w'), 
                             delimiter=';',
                             fieldnames=['id'])

# %% parse raw html files
#  open app list
app_list = csv.DictReader(open(APP_LIST, 'r'), delimiter=';')

apps_processed = []
for app in app_list:
    file_path = path.join(HTMLfilesFolder, app['id'] + '.htm')
    print("Processing file {}".format(file_path))

    # Skip missing files
    if not path.exists(file_path):
        continue

    # Dictionary to hold app privacy labels info
    app_data = {
        'id': app['id'],
        't': {i : 0 for i in data_types},
        'l': {i : 0 for i in data_types},
        'u': {i : 0 for i in data_types}
    }

    # Open raw html file 
    soup = BeautifulSoup(open(file_path).read())

    # Find privacy labels boxes
    privacy_labels_divs = soup.findAll('div', {'class': 'app-privacy__card'})[0:]

    for div in privacy_labels_divs:
        # Extract card title
        usage_type = div.find('h3', {'class':'privacy-type__heading'}).text

        # Extract card contents
        datums = div.findAll('span', {'class':'privacy-type__grid-content'})
        for data in datums: 
            # Update app data dictionary
            app_data[names_map[usage_type]].update({data.text : 1})

    # Flatten the data to save it in .csv
    flattened_app_data = {}
    for key in app_data.keys():
        if key is 'id':
            flattened_app_data.update({'id': app_data['id']})
        else:
            for name in app_data[key].keys():
                flattened_app_data.update({key + name.replace(' ', '') : app_data[key][name]})

    apps_processed.append(flattened_app_data)

# %% Write output to disk

flattened_data_types = ['tHealth&Fitness', 'tLocation', 'tContactInfo', 'tDiagnostics', 'tSensitiveInfo', 'tUsageData', 'tBrowsingHistory', 'tContacts', 'tPurchases', 'tIdentifiers', 'tOtherData', 'tFinancialInfo', 'tSearchHistory', 'tUserContent', 'lHealth&Fitness', 'lLocation', 'lContactInfo', 'lDiagnostics', 'lSensitiveInfo', 'lUsageData', 'lBrowsingHistory', 'lContacts', 'lPurchases', 'lIdentifiers', 'lOtherData', 'lFinancialInfo', 'lSearchHistory', 'lUserContent', 'uHealth&Fitness', 'uLocation', 'uContactInfo', 'uDiagnostics', 'uSensitiveInfo', 'uUsageData', 'uBrowsingHistory', 'uContacts', 'uPurchases', 'uIdentifiers', 'uOtherData', 'uFinancialInfo', 'uSearchHistory', 'uUserContent']

writer = csv.DictWriter(open(OUT_FILE,'w'), fieldnames=['id'] + flattened_data_types, restval=0, delimiter=';')
writer.writeheader()
writer.writerows(apps_processed)

# %%
