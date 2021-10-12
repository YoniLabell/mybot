from flask import Flask, request
import telepot
import urllib3
import requests
from datetime import datetime
import pytz


proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "72c1a1ab-113e-493d-99d4-2e939fcb51e9"
bot = telepot.Bot('1295938032:AAGCrczx5RKq1q20Xi92Z2R914UxutabUYQ')
bot.setWebhook("https://testingtestmail0.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()

    if "message" in update:

        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            if text=='/start':
                wc="ברוך הבא לבוט כדי להריץ אנא התחל עם< כדי לבדוק לינק הכנס לינק"
                bot.sendMessage(chat_id,wc)

            elif text == 'start':

                tz_Israel = pytz.timezone('Israel')
                datetime_Israel = datetime.now(tz_Israel)
                t=datetime_Israel.strftime("%H:%M:%S")
                bot.sendMessage(chat_id,'start: '+str(t))

            elif text == 'end':
                tz_Israel = pytz.timezone('Israel')
                datetime_Israel = datetime.now(tz_Israel)
                t=datetime_Israel.strftime("%H:%M:%S")
                bot.sendMessage(chat_id,'end: '+str(t))

            elif text[0]=='>':
                try:

                    e=eval(text[1:])
                    bot.sendMessage(chat_id,str(e))
                except:
                    bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")

            elif text[0]=="@":

                try:
                    r=requests.get(text)
                    bot.sendMessage(chat_id,str(r.content))
                except:
                    bot.sendMessage(chat_id, "From the web: you said '{}'".format(text))
    else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")
    return "OK"
