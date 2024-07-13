from datetime import datetime, timedelta
import pytz
from src.email_utils import send_email
import yfinance as yf
from matplotlib import pyplot as plt
from io import BytesIO


def send_bist_open():
    tz = pytz.timezone("Europe/Istanbul")
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith("0") else day
    month = today_date.strftime("%B")
    turkish_month = {
        "January": "Ocak",
        "February": "Şubat",
        "March": "Mart",
        "April": "Nisan",
        "May": "Mayıs",
        "June": "Haziran",
        "July": "Temmuz",
        "August": "Ağustos",
        "September": "Eylül",
        "October": "Ekim",
        "November": "Kasım",
        "December": "Aralık",
    }[month]
    xu100 = yf.Ticker("XU100.IS")
    xu100_open = xu100.info.get("open", "")
    xu100_last_close = xu100.info.get("previousClose", "")
    xu100_change = ((xu100_open - xu100_last_close) / xu100_last_close) * 100
    xu100_change = round(xu100_change, 2)
    xu100_open = round(xu100_open, 2)
    emo = "📈" if xu100_change > 0 else "📉"
    text = "yükseliş" if xu100_change > 0 else "düşüş"
    subject = "send_bist100_open #bist"
    body = f"""🔴 #BIST100 {day} {turkish_month} tarihinde güne %{xu100_change} {text} ile başladı.

{emo} Açılış Fiyatı: {xu100_open} \n
    """

    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    stock_data = yf.download("XU100.IS", start=start_date, end=end_date, interval="15m")

    # Resample the data to 3-hour intervals and interpolate to fill missing values
    stock_data_3h = stock_data["Close"].resample("1h").mean().interpolate(method="time")

    # Plotting the graph
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data_3h.index, stock_data_3h.values, linestyle="-")
    plt.title("BIST 100 7-Day Graph (3-Hour Intervals)")
    plt.xlabel("Date")
    plt.ylabel("Price (TL)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    send_email(subject, body, image_stream)
    # print(body)
    # plt.show()


def send_bist_close():
    tz = pytz.timezone("Europe/Istanbul")
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith("0") else day
    month = today_date.strftime("%B")
    turkish_month = {
        "January": "Ocak",
        "February": "Şubat",
        "March": "Mart",
        "April": "Nisan",
        "May": "Mayıs",
        "June": "Haziran",
        "July": "Temmuz",
        "August": "Ağustos",
        "September": "Eylül",
        "October": "Ekim",
        "November": "Kasım",
        "December": "Aralık",
    }[month]
    xu100 = yf.Ticker("XU100.IS")
    xu100_data = xu100.history(period="max")
    xu100_current = xu100_data["Close"][-1]
    xu100_prev = xu100_data["Close"][-2]
    xu100_current_change = ((xu100_current - xu100_prev) / xu100_prev) * 100
    xu100_current_change = round(xu100_current_change, 2)
    xu100_current = round(xu100_current, 2)
    emo = "📈" if xu100_current_change > 0 else "📉"
    text = "yükseliş" if xu100_current_change > 0 else "düşüş"
    subject = "send_bist100_close #bist"
    body = f"""🔴 #BIST100 {day} {turkish_month} tarihinde günü %{xu100_current_change} {text} ile kapattı.

{emo} Kapanış Fiyatı: {xu100_current} \n
    """

    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    stock_data = yf.download("XU100.IS", start=start_date, end=end_date, interval="15m")

    # Resample the data to 3-hour intervals and interpolate to fill missing values
    stock_data_3h = stock_data["Close"].resample("1h").mean().interpolate(method="time")

    # Plotting the graph
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data_3h.index, stock_data_3h.values, linestyle="-")
    plt.title("BIST 100 7-Day Graph (3-Hour Intervals)")
    plt.xlabel("Date")
    plt.ylabel("Price (TL)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    send_email(subject, body, image_stream)


if __name__ == "__main__":
    send_bist_open()
    send_bist_close()
