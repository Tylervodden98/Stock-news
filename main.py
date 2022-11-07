import html
import requests
import os
from dotenv import load_dotenv
import webbrowser
import time
from twilio.rest import Client

load_dotenv(r"../stock-news-extrahard-start/names.env")
# FOR TWILIO MSG
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_URL = "https://www.alphavantage.co/query"
STOCK_KEY = os.getenv("STOCK_KEY")
stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_KEY
}

# Stock api
stock_percentage_change = 0
stock_response = requests.get(STOCK_URL, params=stock_parameters)
data_stock = stock_response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data_stock.items()]


# check if stock increase/decresase
def check_stock():
    increased_stock = yesterday_close * 0.05 + yesterday_close
    decreased_stock = yesterday_close - yesterday_close * 0.05
    global stock_percentage_change
    stock_percentage_change += float((today_close / yesterday_close - 1) * 100).__round__(2)

    if today_close >= increased_stock:
        print(stock_percentage_change)
        print('Get News')

    if today_close <= decreased_stock:
        print(stock_percentage_change)
        print("Get News")


def send_message(article_title, article_description):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"\nReason for stock price drop of {stock_percentage_change}% :\n"
             f"Headline: {article_title}\n"
             f"Brief: {article_description}",
        from_='+14245883985',
        to='+14166164563'
    )


# stock data at close
today_close = float(data_list[0]['4. close'])
yesterday_close = float(data_list[1]['4. close'])
print(today_close)
print(yesterday_close)
check_stock()


NEWS_KEY = os.getenv("NEWS_KEY")
NEWS_URL = "https://newsapi.org/v2/everything"
news_parameters = {
    "q": COMPANY_NAME,
    "apikey": NEWS_KEY
}

news_response = requests.get(NEWS_URL, params=news_parameters)
news_response.raise_for_status()
data_news = news_response.json()
data_news_list = data_news["articles"]

for num in range(0, 3):
    url_data = data_news_list[num]["url"]
    webbrowser.open(url_data)
    article_title = data_news_list[num]["title"]
    article_description = html.escape(data_news_list[num]["description"])
    send_message(article_title, article_description)
    time.sleep(2)
    print(url_data)
    print(article_title)
    print(article_description)


