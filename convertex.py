import requests
import json
import time
import os
import tkinter as tk
from tkinter import messagebox
import pyperclip
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.exchangeratesapi.io/v1/latest?access_key="
CACHE_FILE = 'cache.json'

conversion_rate = {
    'from_currency': 'MXN',
    'to_currency': 'USD'
}

def get_exchange_rate():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        if cache['timestamp'] > time.time() - 24*60*60:
            return cache['rates'][conversion_rate['from_currency']], cache['rates'][conversion_rate['to_currency']]

    response = requests.get(BASE_URL + API_KEY)
    if response.status_code == 200:
        data = json.loads(response.text)
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
        return data['rates'][conversion_rate['from_currency']], data['rates'][conversion_rate['to_currency']]
    else:
        print(f"Error: {response.status_code}")
        return None, None

def convert_currency():
    amount = float(currency_entry.get())
    from_rate, to_rate = get_exchange_rate()
    converted_amount = (amount / from_rate) * to_rate
    result_label['text'] = f'{amount} {conversion_rate["from_currency"]} = {converted_amount:.2f} {conversion_rate["to_currency"]}'
    pyperclip.copy(f'{converted_amount:.2f}')

def toggle_currency():
    conversion_rate['from_currency'], conversion_rate['to_currency'] = conversion_rate['to_currency'], conversion_rate['from_currency']
    currency_label['text'] = f'Enter amount in {conversion_rate["from_currency"]}:'
    convert_currency()

root = tk.Tk()
root.title('Currency Converter')

currency_label = tk.Label(root, text=f'Enter amount in {conversion_rate["from_currency"]}:')
currency_label.pack(padx=10, pady=10)

currency_entry = tk.Entry(root)
currency_entry.pack(padx=10, pady=10)
currency_entry.insert(0, pyperclip.paste())

convert_button = tk.Button(root, text='Convert', command=convert_currency)
convert_button.pack(padx=10, pady=10)

toggle_button = tk.Button(root, text='Toggle Currency', command=toggle_currency)
toggle_button.pack(padx=10, pady=10)

result_label = tk.Label(root, text='')
result_label.pack(padx=10, pady=10)

root.mainloop()
