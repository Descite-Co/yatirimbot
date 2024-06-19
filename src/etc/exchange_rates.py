from io import BytesIO
import yfinance as yf
from matplotlib import pyplot as plt
from src.email_utils import send_email


def get_currency_data(currency_pair):
    return yf.Ticker(currency_pair).history(period="3mo")  # Son 3 ayın verisi


def plot_currency_data(currency_data, currency_pair):
    plt.figure(figsize=(10, 5))
    plt.plot(currency_data['Close'], label='USD/TRY Son Fiyat')
    plt.title('Dolar (USD/TRY) - Son 3 Ay')
    plt.xlabel('Tarih')
    plt.ylabel('Değer')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return plt


def currency_send():
    currencies = ["USDTRY=X", "EURTRY=X", "GBPTRY=X"]
    email_body = "🌍 Döviz Kurları 🌍\n\n"

    image_buffer = BytesIO()
    for currency in currencies:
        data = get_currency_data(currency)
        last_price = data['Close'].iloc[-1]
        change = (data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100
        currency_label = currency.replace("=X", "")

        if currency == "USDTRY=X":
            plt = plot_currency_data(data, currency)
            plt.savefig(image_buffer, format='png')
            plt.close()
            image_buffer.seek(0)

        email_body += f'{currency_label}:\nSon Fiyat: {last_price:.2f}\nDeğişim: {change:.2f}%\n\n'

    send_email("Güncel Döviz Kurları #crypto", email_body, image_buffer)


if __name__ == "__main__":
    currency_send()
