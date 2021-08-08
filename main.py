
import requests
from requests.api import request
from twilio.rest import Client
from authentication_file import stock_api_key,news_api_key,TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_NUMBER_FROM,TWILIO_NUMBER_TO

CRYPTO_SYMBOL = "BTC"
CRYPTO_NAME = "Bitcoin"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api_key = stock_api_key
stock_parameters = {
    "function": "CRYPTO_INTRADAY",
    "symbol": CRYPTO_SYMBOL,
    "apikey": stock_api_key,
    "market": "EUR",
    "interval": '60min',
}

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = news_api_key
new_parameters = {
    "apiKey": news_api_key,
    "qInTitle": CRYPTO_NAME,
    # "q": CRYPTO_NAME,
    "sortBy":"popularity"
}

'''Twilio'''
# TWILIO_ACCOUNT_SID = TWILIO_ACCOUNT_SID
# TWILIO_AUTH_TOKEN = TWILIO_AUTH_TOKEN
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

'''Stocks'''
stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
data = stock_response.json()["Time Series Crypto (60min)"]
data_list = [value for (key,value) in data.items()][:8]
print(data)

closing_price_last = data_list[-1]["4. close"]

closing_price_now = data_list[0]["4. close"]
'''Difference'''
difference = float(closing_price_last) - float(closing_price_now)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference/float(closing_price_last))*100)

'''Articles'''
new_response = requests.get(url=NEWS_ENDPOINT,params=new_parameters)
articles = new_response.json()["articles"]
three_articles = articles[:3]
print(three_articles)
formatted_articles = [f"{CRYPTO_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(formatted_articles)

'''Twilio SMS'''
client = Client(account_sid, auth_token)
for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_=TWILIO_NUMBER_FROM,
        to=TWILIO_NUMBER_TO
    )
print(message.status)
