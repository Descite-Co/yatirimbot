"""
This module generates a performance report for a randomly chosen stock from Borsa İstanbul (BIST).

It retrieves historical data for the stock using the yfinance library and generates a graph of its
price history, as well as calculating percentage changes over specified time periods. The results
are then formatted into a message that can be sent via email.
"""

import random
from io import BytesIO
import matplotlib.pyplot as plt
import yfinance as yf
from src.email_utils import send_email
from src.lib.constants import bist_all
from src.lib.utils import get_stock_emoji_and_text
from src.lib.utils import get_turkish_month


def initialize_stock_data():
    """
    Initialize the stock data by randomly selecting a stock and retrieving its historical data.

    Returns:
        tuple: Contains the chosen stock, stock code, historical data, and the stock information.
    """
    chosen_stock = random.choice(bist_all)
    stock_code = chosen_stock + ".IS"
    chosen_stock_info = yf.Ticker(stock_code)

    # Retrieve historical data for the chosen stock
    hist_data = chosen_stock_info.history(period="1y")

    return chosen_stock, hist_data, chosen_stock_info


def generate_stock_graph(stock, hist_data):
    """
    Generate a line graph of the historical closing prices for the specified stock.

    Args:
        stock (str): The stock code to generate the graph for.
        hist_data (DataFrame): Historical data of the stock.

    Returns:
        BytesIO: A BytesIO object containing the PNG image of the graph.
    """
    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(hist_data["Close"], label="Son Fiyat")
    plt.title(f"{stock} Hisse Senedi Grafiği")
    plt.xlabel("")
    plt.ylabel("Fiyat")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a BytesIO object
    image = BytesIO()
    plt.savefig(image, format="png")  # Save the plot as PNG image to the BytesIO object
    plt.show()
    return image


def bist_stock_by_time():
    """
    Generate a performance report for the chosen stock, including percentage changes over different time periods, and print the report. This function also generates agraph of the stock's historical prices.

    Returns:
        None
    """
    # Initialize stock data
    chosen_stock, hist_data, chosen_stock_info = initialize_stock_data()

    # Get the latest price
    today = chosen_stock_info.info.get("currentPrice", "0")

    # Values for 5-day change
    day_5_close = hist_data["Close"].iloc[-6]
    day_5_change_percent = (((today - day_5_close) / day_5_close) * 100).round(1)
    day_5_day = hist_data.index[-6].strftime("%d")
    day_5_month = hist_data.index[-6].strftime("%B")
    day_5_year = hist_data.index[-6].strftime("%Y")
    turkish_day_5 = get_turkish_month(day_5_month)

    # Values for 1-month change
    month_1_close = hist_data["Close"].iloc[-31]
    month_1_change_percent = (((today - month_1_close) / month_1_close) * 100).round(1)
    month_1_day = hist_data.index[-31].strftime("%d")
    month_1_month = hist_data.index[-31].strftime("%B")
    month_1_year = hist_data.index[-31].strftime("%Y")
    turkish_month_1 = get_turkish_month(month_1_month)

    # Values for 6-month change
    month_6_close = hist_data["Close"].iloc[-181]
    month_6_change_percent = (((today - month_6_close) / month_6_close) * 100).round(1)
    month_6_day = hist_data.index[-181].strftime("%d")
    month_6_month = hist_data.index[-181].strftime("%B")
    month_6_year = hist_data.index[-181].strftime("%Y")
    turkish_month_6 = get_turkish_month(month_6_month)

    image = generate_stock_graph(chosen_stock, hist_data)

    # Construct the message
    body = f"""🔴 #{chosen_stock} Hissesinin Zamana Bağlı Performansı 👇

💸 Güncel Fiyat: {today}

{get_stock_emoji_and_text(day_5_change_percent, "emoji")} {day_5_day} {turkish_day_5} {day_5_year} tarihinden beri %{day_5_change_percent} {get_stock_emoji_and_text(day_5_change_percent, "text")}.
{get_stock_emoji_and_text(month_1_change_percent, "emoji")} {month_1_day} {turkish_month_1} {month_1_year} tarihinden beri %{month_1_change_percent} {get_stock_emoji_and_text(month_1_change_percent, "text")}.
{get_stock_emoji_and_text(month_6_change_percent, "emoji")} {month_6_day} {turkish_month_6} {month_6_year} tarihinden beri %{month_6_change_percent} {get_stock_emoji_and_text(month_6_change_percent, "text")}.

#yatırım #borsa #hisse #ekonomi #bist #bist100 #türkiye #faiz #enflasyon #endeks #finans #para #şirket
          """
    subject = "bist_by_time #bist_stock_by_time"

    # print(body)
    send_email(subject, body, image)


if __name__ == "__main__":
    bist_stock_by_time()
