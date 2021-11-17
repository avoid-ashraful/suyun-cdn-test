import requests

URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
TELEGRAM_BOT_TOKEN = ""
CHAT_ID = ""


def send_telegram_message(text):
    results = requests.get(URL.format(
       TELEGRAM_BOT_TOKEN,
       CHAT_ID,
       text
    ))
    print(results.json())
