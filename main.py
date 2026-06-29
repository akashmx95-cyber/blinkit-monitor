import requests
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime
import telegram

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PINCODE = "110053"

PRODUCTS = [
    {"name": "PS5 Standard", "url": "https://blinkit.com/prn/x/prid/763266"},
    {"name": "PS5 Digital", "url": "https://blinkit.com/prn/x/prid/779739"}
]

def is_in_stock(text):
    out_phrases = ["coming soon", "out of stock", "notify me", "unavailable"]
    t = text.lower()
    return not any(phrase in t for phrase in out_phrases)

def check_product(product):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(product["url"], headers=headers, timeout=20)
        if r.status_code == 200 and is_in_stock(r.text):
            bot = telegram.Bot(token=BOT_TOKEN)
            msg = f"""🚨 **STOCK ALERT - PS5 AVAILABLE!** 🚨

✅ {product['name']} is **IN STOCK** now!
📍 Pincode: {PINCODE}
⏰ {datetime.now().strftime('%d %b, %I:%M %p')}

🔗 {product['url']}

Go buy fast!"""
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
            print(f"✅ ALERT SENT for {product['name']}")
            return True
    except Exception as e:
        print(f"Error: {e}")
    return False

print("🚀 Blinkit PS5 Monitor Started on Railway!")

while True:
    for product in PRODUCTS:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking {product['name']}...")
        check_product(product)
    time.sleep(35)  # Check every ~35 seconds
