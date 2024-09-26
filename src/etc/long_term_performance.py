"""
This module performs a long-term analysis of a randomly selected stock.

It fetches stock data, creates a chart, and sends an email report.
"""
from datetime import datetime, timedelta
from io import BytesIO
from secrets import randbelow

import matplotlib.pyplot as plt
import yfinance as yf

from src.email_utils import send_email
from src.lib.constants import us_stock_list

def format_value(value, currency):
    """Format numerical values with currency."""
    if value and isinstance(value, (int, float)):
        return f"{value:, .2f} {currency}".replace(",", ".")
    return ""

def analyze_long_term_stock():
    """Analyze a randomly selected stock and send a report via email."""
    selected_stock = us_stock_list[randbelow(len(us_stock_list))]
    stock = yf.Ticker(selected_stock)
    stock_info = stock.info
    currency = stock_info.get("financialCurrency", "USD")

    email_body = f"📈#{selected_stock} {stock_info.get('shortName', 'Stock')} hisse senedinin güncel ve uzun dönemli performansı 👇\n\n"
    current_price = stock_info.get("regularMarketPrice") or (stock_info.get("open", 0) + stock_info.get("dayHigh", 0)) / 2
    email_body += f"▪️ Anlık Fiyat: {format_value(current_price, currency)}\n"
    email_body += f"▪️ 52 Haftalık En Yüksek Değer: {format_value(stock_info.get('fiftyTwoWeekHigh'), currency)}\n"
    email_body += f"▪️ Ortalama Günlük İşlem Hacmi (Son 10 Gün): {format_value(stock_info.get('averageDailyVolume10Day'), 'hisse')}\n"
    email_body += f"▪️ Piyasa Değeri: {format_value(stock_info.get('marketCap'), currency)}\n"

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    stock_data = yf.download(selected_stock, start=start_date, end=end_date)

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data["Close"], label="Son Fiyat")
    y_min, y_max = stock_data["Close"].min(), stock_data["Close"].max()
    y_ticks = range(int(y_min), int(y_max) + 1, max(1, int((y_max - y_min) / 10)))
    plt.yticks(y_ticks)
    plt.title(f'{stock_info.get("shortName", selected_stock)} Değişim Grafiği')
    plt.ylabel("Fiyat")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    subject = f"{stock_info.get('shortName', selected_stock)} Hissesi Performans Raporu #L_term_stock"
    send_email(subject, email_body, image_stream)

if __name__ == "__main__":
    analyze_long_term_stock()
