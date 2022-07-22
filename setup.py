import requests
import smtplib
import ssl
#import time
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM
import json


def get_crypto_price(coin_symbol, currency):
    url = "https://min-api.cryptocompare.com/data/price?fsym="+coin_symbol+"&tsyms="+currency
    resp = requests.get(url).json()
    price = resp[currency]
    return price


sender = 'chavanmadhur65@gmail.com'
sender_password = 'Madhur@2565'


def send_email(sender, receiver, sender_password, text_price):
    msg = MM()
    msg['Subject'] = u"\U0001F514"+u"\U0001F514"+u"\U0001F514"+" New Crypto Price Alert !!!"
    msg['From'] = sender
    msg['To'] = receiver

    HTML = """
        <html>
            <body>
                <h1> New Crypto Price Alert !</h1>
                <h2> """+text_price+""" </h2>
            </body>
        </html>
    """
    MTObj = MT(HTML, "html")
    msg.attach(MTObj)

    SSL_context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=SSL_context)

    server.login(sender, sender_password)

    server.sendmail(sender, receiver, msg.as_string())



def send_alert(i):

        btc_price = get_crypto_price('BTC', 'INR')
        eth_price = get_crypto_price('ETH', 'INR')
        f = open('config.json', 'r')
        data = json.load(f)["alerts"]
        json_len = len(list(data))
        f.close()
        if json_len != 0 and i < json_len:
            print(i)
            if data[i]["COIN"] == "BTC":
                if data[i]["Range"] == "up":
                    if btc_price >= data[i]["Target_Price"]:
                        price_text = 'Price of BITCOIN is ' + str(btc_price)
                        send_email(sender, data[i]["email"], sender_password, price_text)
                        with open('config.json', 'r') as jason_file:
                            dic = json.load(jason_file)
                            del dic["alerts"][i]
                        with open('config.json', 'w') as jason_file:
                            json.dump(dic, jason_file)
                elif data[i]["Range"] == "down":
                   if btc_price <= data[i]["Target_Price"]:
                        price_text = 'Price of BITCOIN is ' + str(btc_price)
                        send_email(sender, data[i]["email"], sender_password, price_text)
                        with open('config.json', 'r') as jason_file:
                            dic = json.load(jason_file)
                            del dic["alerts"][i]
                        with open('config.json', 'w') as jason_file:
                            json.dump(dic, jason_file)
            elif data[i]["COIN"] == "ETH":
                if data[i]["Range"] == "up":
                    if eth_price >= data[i]["Target_Price"]:
                        price_text = 'Price of ETHEREUM COIN is ' + eth_price
                        send_email(sender, data[i]["email"], sender_password, price_text)
                        with open('config.json', 'r') as jason_file:
                            dic = json.load(jason_file)
                            del dic["alerts"][i]
                        with open('config.json', 'w') as jason_file:
                            json.dump(dic, jason_file)
                else:
                    if eth_price <= data[i]["Target_Price"]:
                        price_text = 'Price of ETHEREUM COIN is ' + eth_price
                        send_email(sender, data[i]["email"], sender_password, price_text)
                        with open('config.json', 'r') as jason_file:
                            dic = json.load(jason_file)
                            del dic["alerts"][i]
                        with open('config.json', 'w') as jason_file:
                            json.dump(dic, jason_file)

while True:
    with open('config.json', 'r') as z:
        value = json.load(z)["alerts"]
        len_value = len(list(value))
        z.close()
    i = 0
    for i in range(len_value+1):
        send_alert(i)
