#%% 
import requests
import json
import time
import os

API_KEY = "fdee8cd0c45dc867fe867abe247921d4"
BASE_URL = "http://api.exchangeratesapi.io/v1/latest?access_key="
CACHE_FILE = 'cache.json'

def get_exchange_rate():
    if os.path.exists(CACHE_FILE):
        # Read the cache file
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)

        # Check if the data is less than a day old
        if cache['timestamp'] > time.time() - 24*60*60:
            return cache['rates']['USD'], cache['rates']['MXN']

    # Either the cache file doesn't exist or the data is more than a day old,
    # so make a GET request to the Exchange Rates API
    response = requests.get(BASE_URL + API_KEY)

    if response.status_code == 200:
        data = json.loads(response.text)

        # Store the data in the cache file for later use
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)

        return data['rates']['USD'], data['rates']['MXN']
    else:
        print(f"Error: {response.status_code}")
        return None, None

def convert_mxn_to_usd(amount_mxn):
    usd_rate, mxn_rate = get_exchange_rate()

    # Convert from MXN to EUR, then from EUR to USD
    amount_usd = (amount_mxn / mxn_rate) * usd_rate

    return amount_usd

# Test the function
print(convert_mxn_to_usd(100))

# %%
