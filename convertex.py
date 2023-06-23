import requests
import json
import time
import os
import tkinter as tk
from tkinter import messagebox
import pyperclip
from dotenv import load_dotenv

# Load environment variables from .env file
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
    # To remove all non-digit characters from the input, including the dot (".") to convert the input to a floating-point number, you can modify the code as follows:
    amount = float(''.join(filter(lambda x: x.isdigit() or x == '.', amount_entry.get())))


    usd_rate, mxn_rate = get_exchange_rate()

    # Check the toggle status to determine the conversion direction
    if toggle_status.get():
        result = (amount / mxn_rate) * usd_rate
        result_label['text'] = f'{amount} MXN = {result:.2f} USD'
    else:
        result = (amount / usd_rate) * mxn_rate
        result_label['text'] = f'{amount} USD = {result:.2f} MXN'

    pyperclip.copy(f'{result:.2f}')

def toggle_conversion():
    if toggle_status.get():
        toggle_button.config(text='Converting MXN to USD')
    else:
        toggle_button.config(text='Converting USD to MXN')

def paste_from_clipboard():
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, pyperclip.paste())

root = tk.Tk()
root.title('Currency Converter')

toggle_status = tk.BooleanVar()
toggle_status.set(True)

toggle_button = tk.Checkbutton(root, text='Converting MXN to USD', variable=toggle_status, command=toggle_conversion)
toggle_button.pack(pady=10)

amount_label = tk.Label(root, text='Enter amount:')
amount_label.pack(pady=10)

amount_entry = tk.Entry(root)
amount_entry.pack(pady=10)

paste_button = tk.Button(root, text='Paste from clipboard', command=paste_from_clipboard)
paste_button.pack(pady=10)

convert_button = tk.Button(root, text='Convert', command=convert_currency)
convert_button.pack(pady=10)

result_label = tk.Label(root, text='')
result_label.pack(pady=10)

root.mainloop()
