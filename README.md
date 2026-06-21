# Stock News Alert

A Python script that monitors a stock's daily price movement and, when it swings more than 5% in a day, automatically texts you the top related news headlines via SMS.

## How It Works

1. Fetches the stock's daily closing prices using the [Alpha Vantage API](https://www.alphavantage.co/).
2. Calculates the percentage change between yesterday and the day before.
3. If the change exceeds **5%**, fetches the top 3 relevant news articles using the [NewsAPI](https://newsapi.org/).
4. Sends an SMS for each article via [Twilio](https://www.twilio.com/), including the price direction (🔺/🔻), headline, and a brief summary.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/stock-news-alert.git
cd stock-news-alert
```

### 2. Install dependencies

```bash
pip install requests newsapi-python twilio python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
ALPHAVANTAGE_API_KEY=your_alphavantage_key
NEWS_API_KEY=your_newsapi_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=+1234567890
YOUR_PHONE=+1234567890
```

### 4. Run the script

```bash
python main.py
```

## Configuration

By default the script tracks **Tesla (TSLA)**. To track a different stock, edit these variables in `main.py`:

```python
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
```

## Notes

- Designed to be run daily (e.g. via a cron job or scheduled task) to check for significant overnight price moves.
- The 5% threshold can be adjusted by changing the condition in `main.py`.
