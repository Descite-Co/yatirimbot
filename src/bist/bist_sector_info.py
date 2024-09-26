"""
This module provides functionality to fetch and send performance data of random sectors from the Borsa İstanbul (BIST).

It uses the yfinance library to retrieve daily sector performance information and generates a formatted email containing the sector names, their performance percentage changes, and emojis representing the stock's movement.
"""

import random
import yfinance as yf
from src.email_utils import send_email
from src.lib.constants import endeksler
from src.lib.utils import get_date
from src.lib.utils import get_turkish_month
from src.lib.utils import get_stock_emoji_and_text


def fetch_sector_data(index):
    """
    Fetch the daily performance data for a given Borsa İstanbul sector index.

    Args:
        index (str): The sector index code.

    Returns:
        tuple: (long_name, current_price, change, emoji, text)
               Returns information about the sector and its performance.
               If data is unavailable or an error occurs, returns None.
    """
    try:
        stock_code = index + ".IS"
        endeks = yf.Ticker(stock_code)
        endeks_data = endeks.history(period="1d")

        if len(endeks_data) >= 1:
            current = endeks_data["Close"].iloc[-1]
            open_price = endeks_data["Open"].iloc[-1]
            change = ((current - open_price) / open_price) * 100
            change = round(change, 2)
            long_name = endeks.info.get("longName", "Bilgi Yok")
            emo, text = get_stock_emoji_and_text(change)
            return long_name, change, emo, text
        return None  # No sufficient data

    except Exception as error:
        print(f"Error fetching data for {index}: {str(error)}")
        return None


def bist_sector_info():
    """Generate and sends an email report on the performance of random sectors in Borsa İstanbul."""
    today_date = get_date()
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith("0") else day
    month = get_turkish_month(today_date.strftime("%B"))
    random_sectors = random.sample(endeksler, 5)  # Fetch 5 random sectors
    subject = "sektor_hisse_bilgi"
    body = f"""🔴 {day} {month} Borsa İstanbul Endekslerinin Performansları 👇\n\n"""

    for index in random_sectors:
        sector_info = fetch_sector_data(index)
        if sector_info:
            long_name, change, emo, text = sector_info
            body += f"{emo} #{index} {long_name} %{change} {text}.\n"
        else:
            body += f"🔍 #{index} Yeterli veri yok veya veri alınırken hata\n"

    body += "\n#yatırım #borsa #hisse #ekonomi #bist #bist100 #türkiye #faiz #enflasyon #endeks #finans #para #şirket"

    # print(body)
    send_email(subject, body)


if __name__ == "__main__":
    bist_sector_info()
