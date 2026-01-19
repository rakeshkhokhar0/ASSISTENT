import requests

TOKEN = "8439599259:AAEjghkawnP0kF5n9mdBDH0o9IuuEs4a-lY"
CHAT_ID = "6651409150"

msg = "Telegram bot connected successfully."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
