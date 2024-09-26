"""
This module provides functions to fetch and send BIST100 (Istanbul Stock Exchange) data for opening and closing times.

It uses the yfinance library to fetch stock data and the matplotlib library to generate a 7-day graph.
"""

from datetime import datetime, timedelta
import yfinance as yf
from io import BytesIO
from matplotlib import pyplot as plt
from src.email_utils import send_email
from src.lib.utils import get_date
from src.lib.utils import get_turkish_month
from src.lib.utils import get_stock_emoji_and_text


def generate_bist_graph():
    """Generate a 7 day graph with 3 hour intervals for BIST100 Stock Exchange."""
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    stock_data = yf.download("XU100.IS", start=start_date, end=end_date, interval="15m")

    # Resample the data to 3-hour intervals and interpolate to fill missing values
    stock_data_3h = stock_data["Close"].resample("1h").mean().interpolate(method="time")

    # Plotting the graph
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data_3h.index, stock_data_3h.values, linestyle="-")
    plt.title("BIST 100 7 Günlük Grafik")
    plt.xlabel("Tarih")
    plt.ylabel("Fiyat (TL)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    plt.show()
    # image_stream.seek(0)
    return image_stream


def get_bist_open():
    """Fetch the change of BIST100 between previous close and opening."""
    xu100 = yf.Ticker("XU100.IS")
    xu100_open = xu100.info.get("open", "")
    xu100_last_close = xu100.info.get("previousClose", "")
    xu100_change = ((xu100_open - xu100_last_close) / xu100_last_close) * 100
    xu100_change = round(xu100_change, 2)
    xu100_open = round(xu100_open, 2)
    return xu100_open, xu100_change


def send_bist_open():
    """Format the text and send them with a 7 day graph of BIST100."""
    today_date = get_date()
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith("0") else day
    month = get_turkish_month(today_date.strftime("%B"))
    bist_open, bist_change = get_bist_open()
    emo, text = get_stock_emoji_and_text(bist_change)
    subject = "send_bist100_open #bist"
    body = f"""🔴 #BIST100 {day} {month} tarihinde güne %{bist_change} {text} ile başladı.

{emo} Açılış Fiyatı: {bist_open}

#yatırım #borsa #hisse #ekonomi #bist #bist100 #türkiye #faiz #enflasyon #endeks #finans #para #şirket
    """
    image = generate_bist_graph()

    send_email(subject, body, image)
    # print(body)


def get_bist_close():
    """Fetch the current value and previous close value of the exchange and calculate daily change rate."""
    xu100 = yf.Ticker("XU100.IS")
    xu100_data = xu100.history(period="max")
    xu100_current = xu100_data["Close"][-1]
    xu100_prev = xu100_data["Close"][-2]
    xu100_current_change = ((xu100_current - xu100_prev) / xu100_prev) * 100
    xu100_current_change = round(xu100_current_change, 2)
    xu100_current = round(xu100_current, 2)
    return xu100_current, xu100_current_change


def send_bist_close():
    """Format the text and send them with a 7 day graph of BIST100."""
    today_date = get_date()
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith("0") else day
    month = get_turkish_month(today_date.strftime("%B"))
    bist_close, bist_change = get_bist_close()
    emo, text = get_stock_emoji_and_text(bist_change)
    subject = "send_bist100_close #bist"
    body = f"""🔴 #BIST100 {day} {month} tarihinde günü %{bist_change} {text} ile kapattı.

{emo} Kapanış Fiyatı: {bist_close}

#yatırım #borsa #hisse #ekonomi #bist #bist100 #türkiye #faiz #enflasyon #endeks #finans #para #şirket
    """
    image = generate_bist_graph()

    send_email(subject, body, image)
    # print(body)


if __name__ == "__main__":
    send_bist_open()
    send_bist_close()
