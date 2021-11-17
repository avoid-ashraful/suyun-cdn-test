from datetime import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from telegram import send_telegram_message

ADDRESS = "TSaJqQ1AZ2bEYyqBwBmJqCBSPv8KPRTAdv"
TRANSACTION_INFO_URL = "https://api.shasta.trongrid.io/v1/accounts/{}/transactions"
REFRESH_DELAY = 10  # in second
NOTIFICATION_HOUR = 23
NOTIFICATION_MIN = 59

scheduler = BackgroundScheduler()


def get_transaction_info(address):
    url = TRANSACTION_INFO_URL.format(address)
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_transaction_amount(transaction):
    return transaction.get("raw_data", {}).get(
            "contract",
            [{}]
        )[0].get("parameter", {}).get("value", {}).get("amount", 0)


@scheduler.scheduled_job("interval", seconds=REFRESH_DELAY)
def check_new_successful_transaction():
    current_time = datetime.now()
    transactions = get_transaction_info(address=ADDRESS)
    for transaction in transactions.get("data", []):
        transaction_datetime = datetime.fromtimestamp(int(transaction.get("block_timestamp")) / 1e3)
        if (current_time - transaction_datetime).seconds < REFRESH_DELAY:
            send_telegram_message(
                f"New Transaction!\n"
                f"Amount: {get_transaction_amount(transaction)}\n"
            )
    print(f"Checking new successful transaction")


@scheduler.scheduled_job("cron", hour=NOTIFICATION_HOUR, minute=NOTIFICATION_MIN)
def check_daily_transactions():
    total_transaction = 0
    transactions = get_transaction_info(address=ADDRESS)
    for transaction in transactions.get("data", []):
        transaction_datetime = datetime.fromtimestamp(int(transaction.get("block_timestamp")) / 1e3)
        if transaction_datetime.date() == datetime.now().date():
            total_transaction += get_transaction_amount(transaction)
    send_telegram_message(
        f"Total Transaction: {total_transaction}\n"
    )
    print(f"Executing daily transactions checkup")


scheduler.start()
