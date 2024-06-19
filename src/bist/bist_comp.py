from io import BytesIO
from datetime import datetime, timedelta;
import pytz
from matplotlib import pyplot as plt
from src.email_utils import send_email
import yfinance as yf

def bist_comp():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d").lstrip('0')
    month = today_date.strftime("%B")
    turkish_month = {
        "January": "Ocak", "February": "Şubat", "March": "Mart", "April": "Nisan",
        "May": "Mayıs", "June": "Haziran", "July": "Temmuz", "August": "Ağustos",
        "September": "Eylül", "October": "Ekim", "November": "Kasım", "December": "Aralık"
    }[month]

    xu100 = yf.Ticker('XU100.IS')
    xu100_data = xu100.history(period='max')
    xu100_current = xu100_data['Close'].iloc[-1]
    xu100_prev = xu100_data['Close'].iloc[-2]
    xu100_current_change = (((xu100_current - xu100_prev) / xu100_prev) * 100)
    xu100_current = round(xu100_current, 2)
    xu100_current_change = round(xu100_current_change, 2)
    emo100 = '📈' if xu100_current_change > 0 else '📉'

    xu30 = yf.Ticker('XU030.IS')
    xu30_data = xu30.history(period='max')
    xu30_current = xu30_data['Close'].iloc[-1]
    xu30_prev = xu30_data['Close'].iloc[-2]
    xu30_current_change = (((xu30_current - xu30_prev) / xu30_prev) * 100)
    xu30_current = round(xu30_current, 2)
    xu30_current_change = round(xu30_current_change, 2)
    emo30 = '📈' if xu30_current_change > 0 else '📉'

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    stock_data1 = yf.download('XU030.IS', start=start_date, end=end_date)
    stock_data2 = yf.download('XU100.IS', start=start_date, end=end_date)

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data1['Close'], label='XU030.IS', color='blue')
    plt.plot(stock_data2['Close'], label='XU100.IS', color='orange')
    plt.legend()
    plt.title('BIST100 - BIST30 Karşılaştırması')
    plt.xlabel('')
    plt.ylabel('Fiyat (TL)')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    subject = "BIST100 - BIST30 Karşılaştırması"
    body = f"""🔴 BIST100 - BIST30 Karşılaştırması 👇

#BIST30
💸 Anlık Fiyat: {xu30_current} TL
{emo30} Günlük Değişim: %{xu30_current_change}

#BIST100
💸 Anlık Fiyat: {xu100_current} TL
{emo100} Günlük Değişim: %{xu100_current_change}
    """
    # Ensure your email sending functionality is correctly configured
    send_email(subject, body, image_stream)



if __name__ == "__main__":
    bist_comp()