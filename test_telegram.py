import requests
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("telegram_token")
CHAT_ID = os.getenv("chat_id")

msg = "Telegram bot connected successfully."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
