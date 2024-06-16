# main.py
from src.email_utils import send_email
import matplotlib.pyplot as plt
import yfinance as yf
from io import BytesIO
import requests

def plot_bitcoin_graph():
    btc = yf.Ticker("BTC-USD")
    btc_data = btc.history(period="1mo")
    plt.figure(figsize=(10, 5))
    plt.plot(btc_data['Close'], label='Son Fiyat')
    plt.title('Bitcoin Aylık Grafik')
    plt.ylabel('Dolar')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    return image_buffer

def format_price(price):
    return "{:,.2f}".format(float(price))

def format_market_cap(market_cap):
    market_cap = float(market_cap)
    if market_cap < 1_000_000:
        return f"${market_cap:,.0f}"
    elif market_cap < 1_000_000_000:
        return f"${market_cap / 1_000_000:.2f} Milyon"
    elif market_cap < 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f} Milyar"
    else:
        return f"${market_cap / 1_000_000_000_000:.2f} Trilyon"


def get_crypto_price(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print(f"{url} adresine yapılan istek başarısız oldu. Hata kodu:", response.status_code)
        return None

def crypto_send():
    cryptos = {
        "BTC": ["https://cryptoprices.cc/BTC/", "https://cryptoprices.cc/BTC/MCAP/"],
        "ETH": ["https://cryptoprices.cc/ETH/", "https://cryptoprices.cc/ETH/MCAP/"],
        "SOL": ["https://cryptoprices.cc/SOL/", "https://cryptoprices.cc/SOL/MCAP/"]
    }
    body = "🚀 Anlık Kripto Verileri 🚀\n"
    for crypto, urls in cryptos.items():
        price = get_crypto_price(urls[0])
        market_cap = get_crypto_price(urls[1])
        if price is not None and market_cap is not None:
            formatted_price = format_price(price)
            formatted_market_cap = format_market_cap(market_cap)
            body += f"\n🌟 #{crypto} Fiyatı: ${formatted_price}\n"
            body += f"💰 #{crypto} Piyasa Değeri: {formatted_market_cap}\n"

    image_stream = plot_bitcoin_graph()
    send_email("Anlık Kripto Verileri", body, image_stream)

if __name__ == "__main__":
    crypto_send()