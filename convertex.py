import os
import requests
import json
import time
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import pyperclip

# Load .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
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

def convert_currency():
    amount = float(amount_entry.get())
    usd_rate, mxn_rate = get_exchange_rate()

    if currency_var.get() == 'MXN':
        result = (amount / mxn_rate) * usd_rate
        result_label['text'] = f'{amount} MXN = {result:.2f} USD'
    else:
        result = (amount / usd_rate) * mxn_rate
        result_label['text'] = f'{amount} USD = {result:.2f} MXN'

    pyperclip.copy(f'{result:.2f}')

def copy_from_clipboard():
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, pyperclip.paste())

root = tk.Tk()
root.title('Currency Converter')

padding = tk.Frame(root, padx=15, pady=15)
padding.pack()

currency_var = tk.StringVar(value='MXN')

amount_label = tk.Label(padding, text='Enter amount:')
amount_label.pack()

amount_entry = tk.Entry(padding)
amount_entry.pack()
amount_entry.insert(0, pyperclip.paste())

copy_button = tk.Button(padding, text='Copy from clipboard', command=copy_from_clipboard)
copy_button.pack(pady=(5,10))

mxn_radio = tk.Radiobutton(padding, text='MXN to USD', variable=currency_var, value='MXN')
mxn_radio.pack()

usd_radio = tk.Radiobutton(padding, text='USD to MXN', variable=currency_var, value='USD')
usd_radio.pack(pady=(0,10))

convert_button = tk.Button(padding, text='Convert', command=convert_currency)
convert_button.pack()

result_label = tk.Label(padding, text='')
result_label.pack()

root.mainloop()
