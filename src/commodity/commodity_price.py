"""Module for fetching and reporting commodity price information."""

from datetime import datetime, timedelta
from io import BytesIO

import yfinance as yf
from matplotlib import pyplot as plt

from src.email_utils import send_email

def format_currency(price, currency):
    """
    Format the given price with the specified currency.

    Args:
        price (float or str): The price to be formatted.
        currency (str): The currency symbol or code.

    Returns:
        str: Formatted price with currency.
    """
    if isinstance(price, str):
        return price
    return f"{price:.2f} {currency}"

def get_commodity_info(ticker, display_name):
    """
    Fetch and format commodity information.

    Args:
        ticker (str): The commodity ticker symbol.
        display_name (str): The display name of the commodity.

    Returns:
        tuple: A tuple containing commodity info and formatted email body.
    """
    commodity = yf.Ticker(ticker)
    commodity_info = commodity.info
    currency = commodity_info.get("financialCurrency", "USD")
    email_body = f"🔴 {display_name} güncel ve uzun dönemli performansı 👇\n\n"
    current_price = commodity_info.get(
        "regularMarketPrice",
        (commodity_info.get("open", 0) + commodity_info.get("dayHigh", 0)) / 2,
    )
    email_body += f"▪️ Anlık Fiyat: {format_currency(current_price, currency)}\n"
    email_body += f"▪️ 52 Haftalık En Yüksek Değer: {format_currency(commodity_info.get('fiftyTwoWeekHigh', 0), currency)}\n"
    email_body += f"▪️ 52 Haftalık En Düşük Değer: {format_currency(commodity_info.get('fiftyTwoWeekLow', 0), currency)}\n"
    return commodity_info, email_body

def plot_commodity_prices(historical_data, display_name):
    """
    Plot commodity prices and return the image as a BytesIO object.

    Args:
        historical_data (pandas.DataFrame): Historical price data.
        display_name (str): The display name of the commodity.

    Returns:
        BytesIO: An in-memory bytes buffer containing the plot image.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(historical_data["Close"])
    plt.title(f"{display_name} Değişim Grafiği")
    plt.ylabel("Fiyat Dolar")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)
    return image_stream

def commodity_price(ticker, display_name):
    """
    Fetch commodity price information, create a plot, and send an email report.

    Args:
        ticker (str): The commodity ticker symbol.
        display_name (str): The display name of the commodity.
    """
    commodity_info, email_body = get_commodity_info(ticker, display_name)
    historical_data = yf.download(
        ticker,
        start=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        end=datetime.now().strftime("%Y-%m-%d"),
    )
    image_stream = plot_commodity_prices(historical_data, display_name)
    send_email(
        f"Emtia Güncellemesi: {display_name} #commodity_price", email_body, image_stream
    )

if __name__ == "__main__":
    commodity_price("CL=F", "Ham Petrol")  # Crude Oil
    commodity_price("HO=F", "Kalorifer Yakıtı")  # Heating Oil
    commodity_price("NG=F", "Doğal Gaz")  # Natural Gas
