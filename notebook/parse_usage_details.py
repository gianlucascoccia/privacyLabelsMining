# %% Imports

import csv
import os.path as path
import pandas as pd 
import numpy as np
import json
from io import StringIO

# %% params

OUT_FILE = "../data/raw/top_1000_apps_top_grossing_purposes.csv"
IN_FILE = "../data/raw/top_1000_apps_top_grossing_store_data.csv"
IN_FOLDER = "../data/raw/labelsPurpose"

# %% helper vars 

usage_prefixes = ['l', 'u']
purposes = ['app_functionality', 'other_purposes', 'analytics', 'developers_advertising', 'product_personalization', 'third_party_advertising']
data_types = ['diagnostics', 'health_and_fitness', 'financial_info', 'identifiers', 'usage_data', 'browsing_history', 'sensitive_info', 'contact_info', 'user_content', 'other', 'purchases', 'contacts', 'location', 'search_history']

cols = set()
for u in usage_prefixes:
    for p in purposes:
        for d in data_types:
            cols.add(u + '_' + p + '_' + d)

observed_usages = pd.DataFrame(columns=['id'] + list(cols), dtype='Int64')

# %% load app list
 
app_list = pd.read_csv(IN_FILE, ";")

# %% iterate on and parse purposes files

df_rows = []
for index, row in app_list.iterrows():

    # check if app id is valid
    if np.isnan(row['id']):
        continue

    app_name = int(row['id'])
    modal_file_name = "{}_usages.json".format(app_name)

    print("Processing app #{}, {}".format(index, modal_file_name))

    # check if file exists
    in_file_path = path.join(IN_FOLDER, modal_file_name)
    if not path.isfile(in_file_path):
        continue

    # open file
    with open(in_file_path, 'r') as f:
        in_file = json.load(f)
        
        # Check if its placeholder file
        if type(in_file) is dict:
            if in_file['error_type'] == 404:
                continue

        purpose_file = json.loads(in_file)

        usages_row = {
            'id': app_name
        }
        
        # navigate to relevant elements
        for item in purpose_file['data']:
            for privacy_type in item['attributes']['privacyDetails']['privacyTypes']:   
                
                # Check type of data
                if privacy_type['identifier'] == 'DATA_NOT_COLLECTED':
                    continue
                elif privacy_type['identifier'] == 'DATA_USED_TO_TRACK_YOU':
                    prefix = 't_'
                elif privacy_type['identifier'] == 'DATA_LINKED_TO_YOU':
                    prefix = 'l_'
                elif privacy_type['identifier'] == 'DATA_NOT_LINKED_TO_YOU':
                    prefix = 'u_'    

                # Iterate on purposes
                for purpose in privacy_type['purposes']:
                    
                    # Check purpose type
                    typed_purpose = prefix + purpose['identifier'].lower()

                    # Data used for this purpose
                    for category in purpose['dataCategories']:
                        typed_purpose_usage = typed_purpose + '_' + category['identifier'].lower() 

                        usages_row.update({typed_purpose_usage:1})

                    # TODO: individual datums affected

    # Update processed items
    df_rows.append(usages_row)

# %% update results data frame                    

observed_usages = observed_usages.append(df_rows)
observed_usages = observed_usages.fillna(0)

# %% write output

observed_usages.to_csv(OUT_FILE)
