from io import BytesIO
import yfinance as yf
from matplotlib import pyplot as plt
from src.email_utils import send_email


def get_silver_data():
    silver = yf.Ticker("SI=F")
    return silver.history(period="max")


def plot_silver_data(silver_data):
    plt.figure(figsize=(12, 6))
    plt.plot(silver_data["Close"], label="Gümüş Son Fiyat ($)")
    plt.title("Tarihsel Gümüş Fiyatları")
    plt.xlabel("Tarih")
    plt.ylabel("Fiyat ($)")  # Dolar cinsinden fiyatlar
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt


def calculate_daily_change(silver_data):
    if len(silver_data) > 1:
        last_close = silver_data["Close"].iloc[-1]
        prev_close = silver_data["Close"].iloc[-2]
        daily_change_percent = (last_close - prev_close) / prev_close * 100
        return daily_change_percent
    else:
        return 0  # Eğer yeterli veri yoksa, değişim 0 olarak kabul edilebilir


def silver():
    silver_data = get_silver_data()
    if not silver_data.empty:
        last_price = silver_data["Close"].iloc[-1]
        daily_change = calculate_daily_change(silver_data)

        email_body = "🔴 #Gümüş:\n"
        email_body += (
            f"Son Fiyat: ${last_price:.2f}\nGünlük Değişim: {daily_change:.2f}%\n"
        )

        plt = plot_silver_data(silver_data)
        image_stream = BytesIO()
        plt.savefig(image_stream, format="png")
        plt.close()
        image_stream.seek(0)

        send_email("Güncel Gümüş Fiyatları #silver", email_body, image_stream)
    else:
        print("Gümüş verisi bulunamadı.")


if __name__ == "__main__":
    silver()
