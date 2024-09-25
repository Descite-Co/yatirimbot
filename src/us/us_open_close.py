"""
This module provides functions to fetch and send US market data for opening and closing times.

It uses the yfinance library to fetch market data and a custom email utility to send the information.
"""
from datetime import datetime
import pytz
import yfinance as yf
from src.email_utils import send_email
from src.lib.utils import get_turkish_month

def get_market_data(ticker):
    """Fetch market data for a given ticker."""
    ticker_data = yf.Ticker(ticker)
    current = ticker_data.info.get('open', 0)
    previous = ticker_data.info.get('previousClose', 0)
    change = round(((current - previous) / previous) * 100, 2)
    return current, previous, change

def format_market_data(name, change):
    """Format market data for email body."""
    emoji = "📈" if change > 0 else "📉"
    return f"\n{emoji} {name}: %{change}"

def us_open():
    """Fetch and send US market opening data."""
    turkey_tz = pytz.timezone("Europe/Istanbul")
    today = datetime.now(turkey_tz)
    day = today.strftime("%d").lstrip("0")
    month = get_turkish_month(today.strftime("%B"))

    subject = "send_us_open #us"
    body = f"🔴 {day} {month} ABD Endeksleri Açılış Verileri 👇\n\n"

    for ticker, name in [("^IXIC", "NASDAQ"), ("^GSPC", "S&P 500"), ("^DJI", "Dow Jones")]:
        _, _, change = get_market_data(ticker)
        body += format_market_data(name, change)

    body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"
    send_email(subject, body)

def us_close():
    """Fetch and send US market closing data."""
    turkey_tz = pytz.timezone("Europe/Istanbul")
    today = datetime.now(turkey_tz)
    day = today.strftime("%d").lstrip("0")
    month = get_turkish_month(today.strftime("%B"))

    subject = "send_us_close #us"
    body = f"🔴 {day} {month} ABD Endeksleri Kapanış Verileri 👇\n\n"

    for ticker, name in [("^IXIC", "NASDAQ"), ("^GSPC", "S&P 500"), ("^DJI", "Dow Jones")]:
        ticker_data = yf.Ticker(ticker).history(period="max")
        current = ticker_data["Close"].iloc[-1]
        previous = ticker_data["Close"].iloc[-2]
        change = round(((current - previous) / previous) * 100, 2)
        body += format_market_data(name, change)

    body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"
    send_email(subject, body)

if __name__ == "__main__":
    us_open()
    us_close()
