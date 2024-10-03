"""
This module provides functionality to fetch, analyze, and report silver price data.

It includes functions to retrieve historical silver price data, plot the data,
calculate daily price changes, and send email reports with the analysis.
"""

from io import BytesIO
import yfinance as yf
from matplotlib import pyplot as plt
from src.email_utils import send_email


def get_silver_data():
    """
    Fetch historical silver price data.

    Returns:
        pandas.DataFrame: Historical silver price data.
    """
    silver_ticker = yf.Ticker("SI=F")
    return silver_ticker.history(period="max")


def plot_silver_data(silver_data):
    """
    Create a plot of historical silver prices.

    Args:
        silver_data (pandas.DataFrame): Historical silver price data.

    Returns:
        matplotlib.pyplot: The plot object.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(silver_data["Close"], label="Gümüş Son Fiyat ($)")
    ax.set_title("Tarihsel Gümüş Fiyatları")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Fiyat ($)")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt


def calculate_daily_change(silver_data):
    """
    Calculate the daily percentage change in silver price.

    Args:
        silver_data (pandas.DataFrame): Historical silver price data.

    Returns:
        float: Daily percentage change in price.
    """
    if len(silver_data) > 1:
        last_close = silver_data["Close"].iloc[-1]
        prev_close = silver_data["Close"].iloc[-2]
        return (last_close - prev_close) / prev_close * 100
    return 0  # If there's not enough data, assume no change


def analyze_silver_prices():
    """Analyze silver prices, generate a report, and send it via email."""
    silver_data = get_silver_data()
    if silver_data.empty:
        print("Gümüş verisi bulunamadı.")
        return

    last_price = silver_data["Close"].iloc[-1]
    daily_change = calculate_daily_change(silver_data)

    email_body = (
        "🔴 #Gümüş:\n"
        f"Son Fiyat: ${last_price:.2f}\n"
        f"Günlük Değişim: {daily_change:.2f}%\n"
    )

    silver_plot = plot_silver_data(silver_data)
    image_stream = BytesIO()
    silver_plot.savefig(image_stream, format="png")
    silver_plot.close()
    image_stream.seek(0)

    send_email("Güncel Gümüş Fiyatları #silver", email_body, image_stream)


if __name__ == "__main__":
    analyze_silver_prices()
