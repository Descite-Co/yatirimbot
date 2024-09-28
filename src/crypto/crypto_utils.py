"""Utility functions for fetching and processing cryptocurrency data."""

from io import BytesIO
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import requests
import yfinance as yf

from src.email_utils import send_email

def plot_bitcoin_graph() -> BytesIO:
    """Generate a monthly Bitcoin price graph and return it as a BytesIO object."""
    btc = yf.Ticker("BTC-USD")
    btc_data = btc.history(period="1mo")
    plt.figure(figsize=(10, 5))
    plt.plot(btc_data["Close"], label="Son Fiyat")
    plt.title("Bitcoin Aylık Grafik")
    plt.ylabel("Dolar")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format="png")
    image_buffer.seek(0)
    return image_buffer

def format_price(price: float) -> str:
    """Format the given price with two decimal places and thousands separator."""
    return f"{price:,.2f}"

def format_market_cap(market_cap: float) -> str:
    """Format the market cap value with appropriate suffixes (Million, Billion, Trillion)."""
    if market_cap < 1_000_000:
        return f"${market_cap:,.0f}"
    if market_cap < 1_000_000_000:
        return f"${market_cap / 1_000_000:.2f} Milyon"
    if market_cap < 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f} Milyar"
    return f"${market_cap / 1_000_000_000_000:.2f} Trilyon"

def get_crypto_price(url: str) -> Optional[str]:
    """Fetch cryptocurrency price or market cap from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"{url} adresine yapılan istek başarısız oldu. Hata: {e}")
        return None

def crypto_send() -> None:
    """Fetch cryptocurrency data, format it, and send an email with the information."""
    cryptos: Dict[str, List[str]] = {
        "BTC": ["https://cryptoprices.cc/BTC/", "https://cryptoprices.cc/BTC/MCAP/"],
        "ETH": ["https://cryptoprices.cc/ETH/", "https://cryptoprices.cc/ETH/MCAP/"],
        "SOL": ["https://cryptoprices.cc/SOL/", "https://cryptoprices.cc/SOL/MCAP/"],
    }
    
    body = "🚀 Anlık Kripto Verileri 🚀\n"
    
    for crypto, urls in cryptos.items():
        price, market_cap = map(get_crypto_price, urls)
        if price and market_cap:
            formatted_price = format_price(float(price))
            formatted_market_cap = format_market_cap(float(market_cap))
            body += f"\n🌟 #{crypto} Fiyatı: ${formatted_price}\n"
            body += f"💰 #{crypto} Piyasa Değeri: {formatted_market_cap}\n"
    
    image_stream = plot_bitcoin_graph()
    send_email("Anlık Kripto Verileri #crypto_send", body, image_stream)

if __name__ == "__main__":
    crypto_send()
