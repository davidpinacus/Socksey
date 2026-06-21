import requests
from newsapi import NewsApiClient
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOK = os.getenv('TWILIO_AUTH_TOKEN')

NEWS_API = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey={os.getenv('ALPHAVANTAGE_API_KEY')}"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

response = requests.get(STOCK_ENDPOINT)
data = response.json()

dates=[date for date in data["Time Series (Daily)"].keys()]
yesterday_date=dates[0]
day_before_yesterday_date=dates[1]

yesterday_date_price=data["Time Series (Daily)"][yesterday_date]["4. close"]
day_before_yesterday_date_price=data["Time Series (Daily)"][day_before_yesterday_date]["4. close"]

price_difference=abs(float(yesterday_date_price) - float(day_before_yesterday_date_price))
percentage_diff=(price_difference / float(day_before_yesterday_date_price)) * 100

if percentage_diff > 5:

    all_articles = NEWS_API.get_everything(

            q=COMPANY_NAME,
            sources='bbc-news,the-verge',
            from_param=day_before_yesterday_date,
            to=yesterday_date,
            language='en',
            sort_by='relevancy',
            page=1

        )

    main_articles=all_articles["articles"][:3]

    articles_summary=[(articles["title"], articles["description"])  for articles in main_articles]

    if float(yesterday_date_price) > float(day_before_yesterday_date_price):
        direction = "🔺"
    else:
        direction = "🔻"

    client=Client(TWILIO_ACCOUNT_SID, AUTH_TOK)
    for title, description in articles_summary:
        message_format=f"{STOCK_NAME}: {direction}{int(percentage_diff)}%\nHeadline: {title}\nBrief: {description}"

        message=client.messages.create(
            from_=os.getenv('TWILIO_PHONE'),
            body=message_format,
            to=os.getenv('YOUR_PHONE')
        )

