"""
BIST100 and BIST30 Comparison Script.

This script retrieves stock market data for the BIST100 and BIST30 indices,
generates a comparison plot, and sends an email with the results.
"""

from io import BytesIO
from datetime import datetime, timedelta
from typing import Tuple
import yfinance as yf
import matplotlib.pyplot as plt
from src.email_utils import send_email

def get_stock_data(ticker: str) -> Tuple[float, float, str]:
    """
    Retrieve stock data for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Tuple[float, float, str]: Current price, percentage change, and emoji indicator.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period="2d")
    current = data["Close"].iloc[-1]
    prev = data["Close"].iloc[-2]
    change = ((current - prev) / prev) * 100
    emoji = "📈" if change > 0 else "📉"
    return round(current, 2), round(change, 2), emoji

def plot_comparison(xu30_data: yf.Ticker, xu100_data: yf.Ticker) -> BytesIO:
    """
    Generate a comparison plot of XU030.IS and XU100.IS.

    Args:
        xu30_data (yf.Ticker): BIST30 stock data.
        xu100_data (yf.Ticker): BIST100 stock data.

    Returns:
        BytesIO: A buffer containing the plot image.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(xu30_data["Close"], label="XU030.IS", color="blue")
    plt.plot(xu100_data["Close"], label="XU100.IS", color="orange")
    plt.legend()
    plt.title("BIST100 - BIST30 Karşılaştırması")
    plt.xlabel("")
    plt.ylabel("Fiyat (TL)")
    plt.grid(True)
    plt.tight_layout()

    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)
    return image_stream

def bist_comp():
    """Compare BIST100 and BIST30 indices and send an email report."""
    xu100_current, xu100_change, emo100 = get_stock_data("XU100.IS")
    xu30_current, xu30_change, emo30 = get_stock_data("XU030.IS")

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    xu30_data = yf.download("XU030.IS", start=start_date, end=end_date)
    xu100_data = yf.download("XU100.IS", start=start_date, end=end_date)

    image_stream = plot_comparison(xu30_data, xu100_data)

    subject = "BIST100 - BIST30 Karşılaştırması #bist_comp"
    body = f"""🔴 BIST100 - BIST30 Karşılaştırması 👇

#BIST30
💸 Anlık Fiyat: {xu30_current} TL
{emo30} Günlük Değişim: %{xu30_change}

#BIST100
💸 Anlık Fiyat: {xu100_current} TL
{emo100} Günlük Değişim: %{xu100_change}
    """
    send_email(subject, body, image_stream)

if __name__ == "__main__":
    bist_comp()
