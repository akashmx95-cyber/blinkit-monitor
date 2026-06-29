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
    out_phrases = ["coming soon", "out of stock", "notify me", "unavailable", "comingsoon"]
    t = text.lower()
    return not any(phrase in t for phrase in out_phrases)

def check_product(product):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        r = requests.get(product["url"], headers=headers, timeout=15)
        
        if r.status_code == 200 and is_in_stock(r.text):
            bot = telegram.Bot(token=BOT_TOKEN)
            msg = f"""🚨 **URGENT STOCK ALERT** 🚨

✅ **{product['name']} IS IN STOCK NOW!**

📍 Pincode: {PINCODE}
⏰ {datetime.now().strftime('%d %b, %I:%M:%S %p')}
🔗 {product['url']}

⚡ Buy immediately before it sells out!"""
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
            print(f"🚨 ALERT SENT: {product['name']}")
            return True
    except:
        pass
    return False

print("🚀 Fast Blinkit PS5 Monitor Started (20 sec interval)")

while True:
    for product in PRODUCTS:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking {product['name']}...")
        if check_product(product):
            time.sleep(5)  # Small pause after alert
    time.sleep(20)   # Check every 20 seconds
