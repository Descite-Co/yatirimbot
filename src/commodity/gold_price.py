"""
This module fetches and sends gold price data, including a historical price chart.

It uses the CollectAPI for current gold prices and yfinance for historical data.
"""
import http.client
import json
from io import BytesIO
from datetime import datetime

import pytz
import matplotlib.pyplot as plt
import yfinance as yf

from src.email_utils import send_email
from src.lib.utils import get_turkish_month

def fetch_gold_data():
    """Fetch current gold price data from CollectAPI."""
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        "content-type": "application/json",
        "authorization": "apikey 1XxDAz4EtnKZ099rPKM8Jj:2se49tU9ttxzlhy1KGI5sW",
    }
    conn.request("GET", "/economy/goldPrice", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

def create_gold_chart():
    """Create a chart of historical gold prices."""
    gold = yf.Ticker("GC=F")
    hist_data = gold.history(period="1y")

    plt.figure(figsize=(12, 6))
    plt.plot(hist_data["Close"], label="Son Fiyat")
    plt.legend()
    plt.title("Ons Altın Grafiği")
    plt.ylabel("Fiyat Dolar")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)
    return image_stream

def gold_price():
    """Fetch gold price data, create a chart, and send an email."""
    turkey_tz = pytz.timezone("Europe/Istanbul")
    today_date = datetime.now(turkey_tz)
    day = today_date.strftime("%d").lstrip("0")
    month = get_turkish_month(today_date.strftime("%B"))

    parsed_data = fetch_gold_data()
    image_stream = create_gold_chart()

    subject = f"🔴 Altın Fiyatları {day} {month} #gold_price"
    body = "🔴 Altın Fiyatları:\n\n"
    for item in parsed_data["result"]:
        if item["name"] in ["Gram Altın", "ONS Altın", "Çeyrek Altın"]:
            body += f"💰 {item['name']}: Alış - {item['buying']}, Satış - {item['selling']}\n"

    send_email(subject, body, image_stream)

if __name__ == "__main__":
    gold_price()
    logger.info('Gold Price Function Worked')
