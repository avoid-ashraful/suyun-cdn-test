# suyun-cdn-test

This repo contains the code which will:

Trace TRC20 transactions of the address XXX. Send a telegram notification when the transaction is confirmed , and send a daily summary of the transaction including total in, total out, and net.


# Instruction to run the code:

* Have a python3.8 environment ready.
* Install dependencies "pip install -r requirements.txt"
* Replace your "TELEGRAM_BOT_TOKEN" and "CHAT_ID" in telegram.py file
* Run the project "python main.py"