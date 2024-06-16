import matplotlib.pyplot as plt
import yfinance as yf
from io import BytesIO
import random
from datetime import datetime, timedelta
from src.email_utils import send_email

stock_list = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'BRK.A', 'BRK.B', 'JPM', 'JNJ', 'V', 'PG', 'NVDA', 'MA', 'HD', 'DIS', 'UNH', 'PYPL', 'BAC', 'CMCSA', 'XOM', 'INTC', 'ADBE', 'NFLX', 'T', 'CRM', 'ABT', 'CSCO', 'VZ', 'KO', 'MRK', 'PFE', 'PEP', 'WMT', 'CVX', 'MCD', 'TMO', 'WFC', 'ABBV', 'ORCL', 'AMGN', 'NKE', 'ACN', 'IBM', 'QCOM', 'TXN', 'COST', 'LLY', 'HON', 'MDT', 'AVGO', 'DHR', 'NEE', 'UPS', 'LIN', 'SBUX', 'LOW', 'UNP', 'BA', 'MO', 'MMM', 'RTX', 'GS', 'BDX', 'CAT', 'ADP', 'LMT', 'CVS', 'CI', 'DE', 'ANTM', 'SO', 'BMY', 'USB', 'AXP', 'GILD', 'MS', 'ISRG', 'CHTR', 'RTX', 'PLD', 'AEP', 'TGT', 'D', 'DUK', 'BKNG', 'SPGI', 'VRTX', 'ZTS', 'CME', 'COF', 'CSX', 'CCI', 'REGN', 'CL']

def duzenle(deger, para):
    if deger != 0 and isinstance(deger, int):
        return "{:,.0f} {}".format(deger, para).replace(",", ".")
    elif deger != 0 and isinstance(deger, float):
        return "{:,.2f} {}".format(deger, para).replace(",", ".")
    else:
        return ''

def L_term_stock():
    secilen_hisse = random.choice(stock_list)
    hisse = yf.Ticker(secilen_hisse)
    hisse_bilgileri = hisse.info
    currency = hisse_bilgileri["financialCurrency"]

    email_body = f"📈#{secilen_hisse} {hisse_bilgileri['shortName']} hisse senedinin güncel ve uzun dönemli performansı 👇\n\n"
    anlik_fiyat = hisse_bilgileri.get('regularMarketPrice',
                                      (hisse_bilgileri.get('open', 0) + hisse_bilgileri.get('dayHigh', 0)) / 2)
    email_body += f"▪️ Anlık Fiyat: {duzenle(anlik_fiyat if anlik_fiyat != 0 else '', currency)}\n"
    email_body += f"▪️ 52 Haftalık En Yüksek Değer: {duzenle(hisse_bilgileri.get('fiftyTwoWeekHigh', 0), currency)}\n"
    email_body += f"▪️ Ortalama Günlük İşlem Hacmi (Son 10 Gün): {duzenle(hisse_bilgileri.get('averageDailyVolume10Day', 'hisse'), currency)}\n"
    email_body += f"▪️ Piyasa Değeri: {duzenle(hisse_bilgileri.get('marketCap', 0), currency)}\n"

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    # Download historical stock data for the last year
    stock_data1 = yf.download(secilen_hisse, start=start_date, end=end_date)

    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data1['Close'], label='Son Fiyat')
    y_min = stock_data1['Close'].min()
    y_max = stock_data1['Close'].max()
    y_ticks = range(int(y_min), int(y_max) + 1, 10)
    plt.yticks(y_ticks)
    plt.title(f'{hisse_bilgileri["shortName"]} Değişim Grafiği ')
    plt.ylabel('Fiyat')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # E-posta gönder
    subject = f"{hisse_bilgileri['shortName']} Hissesi Performans Raporu"
    send_email(subject, email_body, image_stream)

if __name__ == "__main__":
    L_term_stock()
