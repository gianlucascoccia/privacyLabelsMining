# %% imports

import pandas as pd
import asyncio
from pyppeteer import launch
import os.path as path
import requests
import json
import numpy as np

# %% params

IN_FILE = "../data/raw/top_1000_apps_free_store_data.csv"
outFolder = "../data/raw/labelsPurpose"

# %% load app list
app_list = pd.read_csv(IN_FILE, delimiter=";")

# %% iterate and dowload modal for each app

for index, row in app_list.iterrows():
    print("Processing app #{}".format(index))

    # check if app id is valid
    if np.isnan(row['id']):
        continue

    app_name = int(row['id'])
    modal_file_name = "{}_usages.json".format(app_name)

    # check if file exists
    out_file_path = path.join(outFolder, modal_file_name)
    if path.isfile(out_file_path):
        continue

    app_url = row['url']
    if len(app_url) == 0:
        continue 

    referer = app_url.split('?')[0]

    # set up authentication request 
    headers = {
    'authority': 'amp-api.apps.apple.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': '*/*',
    'access-control-request-method': 'GET',
    'access-control-request-headers': 'authorization',
    'origin': 'https://apps.apple.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-fetch-dest': 'empty',
    'referer': referer,
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('platform', 'web'),
        ('fields', 'privacyDetails'),
        ('l', 'en-US'),
    )

    # perform authentication request
    response = requests.options('https://amp-api.apps.apple.com/v1/catalog/US/apps/{}'.format(app_name), headers=headers, params=params)

    # set up content retrieval request
    import requests

    headers = {
        'authority': 'amp-api.apps.apple.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json',
        'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlU4UlRZVjVaRFMifQ.eyJpc3MiOiI3TktaMlZQNDhaIiwiaWF0IjoxNjE3NjUzNDg0LCJleHAiOjE2MjA2Nzc0ODR9.q1pNek7PHlAjadqdzwiqB6nSbUF8-gTNJn1aTpGfPNCRwx1JKFBUaaglaeDgirJgCi_BZENkylqwr1EyUc9Mrg',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://apps.apple.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': referer,
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = requests.get('https://amp-api.apps.apple.com/v1/catalog/US/apps/{}'.format(app_name), headers=headers, params=params)

    if response.status_code != 200:
        print("Error {} retrieving data for app {}".format(response.status_code, app_name))
        
        # app no longer exists, write a dummy file
        if response.status_code == 404:
            with open(out_file_path, 'w') as f:
                json.dump({'error_type':404}, f, indent=4)    

        if response.status_code == 429:
            print("API rate excedeed")
            break

        continue

    with open(out_file_path, 'w') as f:
        json.dump(response.text, f, indent=4)    



# %% iterate and dowload modal for each app

#for index, row in app_list.iterrows():
#    print("Processing app #{}".format(index))

#    app_name = row['id']
#    modal_file_name = "{}_modal.htm".format(app_name)

    # check if file exists
#    out_file_path = path.join(outFolder, modal_file_name)
#    if path.isfile(out_file_path):
#        continue

    # check if we have a valid app url
#    app_url = row['url']
#    if len(app_url) == 0:
#        continue 

    # Open puppeteer
#    browser = await launch(headless=False)
    
    # Load app page
#    page = await browser.newPage()
#    await page.goto(app_url, waitUntil='domcontentloaded')

    # Click modal button
#    await page.click('.app-privacy--modal > .we-modal__show')

    # Retrieve modal content
    #await page.waitForSelector('we-modal__content__wrapper')


# %%
