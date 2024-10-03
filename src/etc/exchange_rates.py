"""Module for fetching currency data and sending email reports."""
from io import BytesIO
import yfinance as yf
from matplotlib import pyplot as plt
from src.email_utils import send_email

def get_currency_data(currency_pair: str) -> yf.Ticker.history:
    """
    Fetch the last 3 months of historical data for a given currency pair.

    Args:
        currency_pair (str): The currency pair to fetch data for (e.g., "USDTRY=X").

    Returns:
        yf.Ticker.history: Historical data for the currency pair.
    """
    return yf.Ticker(currency_pair).history(period="3mo")

def plot_currency_data(currency_data: yf.Ticker.history, currency_pair: str) -> plt.Figure:
    """
    Create a plot of the currency data.

    Args:
        currency_data (yf.Ticker.history): Historical data for the currency pair.
        currency_pair (str): The currency pair being plotted.

    Returns:
        plt.Figure: The matplotlib figure containing the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(currency_data["Close"], label=f"{currency_pair} Son Fiyat")
    ax.set_title(f"{currency_pair} - Son 3 Ay")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Değer")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

def currency_send():
    """Fetch currency data, create plots, and send an email report."""
    currencies = ["USDTRY=X", "EURTRY=X", "GBPTRY=X"]
    email_body = "🌍 Döviz Kurları 🌍\n\n"

    image_buffer = BytesIO()
    for currency in currencies:
        data = get_currency_data(currency)
        last_price = data["Close"].iloc[-1]
        change = (
            (data["Close"].iloc[-1] - data["Close"].iloc[0])
            / data["Close"].iloc[0]
            * 100
        )
        currency_label = currency.replace("=X", "")

        if currency == "USDTRY=X":
            fig = plot_currency_data(data, currency_label)
            fig.savefig(image_buffer, format="png")
            plt.close(fig)
            image_buffer.seek(0)

        email_body += f"{currency_label}:\nSon Fiyat: {last_price:.2f}\nDeğişim: {change:.2f}%\n\n"

    send_email("Güncel Döviz Kurları #currency_send", email_body, image_buffer)

if __name__ == "__main__":
    currency_send()
