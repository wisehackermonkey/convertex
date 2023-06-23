import requests
import json
import time
import os
import tkinter as tk
from tkinter import messagebox
import pyperclip

API_KEY = "fdee8cd0c45dc867fe867abe247921d4"
BASE_URL = "http://api.exchangeratesapi.io/v1/latest?access_key="
CACHE_FILE = 'cache.json'

def get_exchange_rate():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        if cache['timestamp'] > time.time() - 24*60*60:
            return cache['rates']['USD'], cache['rates']['MXN']

    response = requests.get(BASE_URL + API_KEY)
    if response.status_code == 200:
        data = json.loads(response.text)
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
        return data['rates']['USD'], data['rates']['MXN']
    else:
        print(f"Error: {response.status_code}")
        return None, None

def convert_mxn_to_usd():
    amount_mxn = float(mxn_entry.get())
    usd_rate, mxn_rate = get_exchange_rate()
    amount_usd = (amount_mxn / mxn_rate) * usd_rate
    result_label['text'] = f'{amount_mxn} MXN = {amount_usd:.2f} USD'
    pyperclip.copy(f'{amount_usd:.2f}')

root = tk.Tk()
root.title('MXN to USD Converter')

mxn_label = tk.Label(root, text='Enter amount in MXN:')
mxn_label.pack()

mxn_entry = tk.Entry(root)
mxn_entry.pack()
mxn_entry.insert(0, pyperclip.paste())  # Insert the current clipboard content into the text box

convert_button = tk.Button(root, text='Convert', command=convert_mxn_to_usd)
convert_button.pack()

result_label = tk.Label(root, text='')
result_label.pack()

root.mainloop()
