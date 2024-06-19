import http
import json
from io import BytesIO
from datetime import datetime, timedelta;
import pytz
from matplotlib import pyplot as plt
from src.email_utils import send_email
import yfinance as yf


def gold_price():
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 1XxDAz4EtnKZ099rPKM8Jj:2se49tU9ttxzlhy1KGI5sW"
    }
    conn.request("GET", "/economy/goldPrice", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)

    # Bugünün tarihini al ve gün ve ayı ayrı değişkenlere at
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day
    month = today_date.strftime("%B")
    turkish_month = {
        "January": "Ocak",
        "February": "Şubat",
        "March": "Mart",
        "April": "Nisan",
        "May": "Mayıs",
        "June": "Haziran",
        "July": "Temmuz",
        "August": "Ağustos",
        "September": "Eylül",
        "October": "Ekim",
        "November": "Kasım",
        "December": "Aralık"
    }[month]

    gold = yf.Ticker('GC=F')
    hist_data = gold.history(period='1y')

    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(hist_data['Close'], label='Son Fiyat')
    plt.legend()
    plt.title('Ons Altın Grafiği')
    plt.ylabel('Fiyat Dolar')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # E-posta oluşturma işlemi
    subject = f"🔴 Altın Fiyatları {day} {turkish_month}"
    body = "🔴 Altın Fiyatları:\n\n"
    for item in parsed_data["result"]:
        if item["name"] in ["Gram Altın", "ONS Altın", "Çeyrek Altın"]:
            body += f"💰 {item['name']}: Alış - {item['buying']}, Satış - {item['selling']}\n"

    send_email(subject, body, image_stream)

if __name__ == "__main__":
    gold_price()