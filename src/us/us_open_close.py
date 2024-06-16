from datetime import datetime;
import pytz
from src.email_utils import send_email
import yfinance as yf

# TODO: Hata veriyor ama paylaşıyor anlamadım
# TODO: İkisinin attığı mailler aynı değil

def us_open():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day
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
        "December": "Aralık"
    }[month]
    subject = ("send_us_open #test ##test")
    body = f"""🔴 {day} {turkish_month} ABD Endeksleri Açılış Verileri 👇

    """
    nasdaq = "^IXIC"
    nasdaq_name = "Nasdaq"
    nasdaq_ticker = yf.Ticker(nasdaq)
    nasdaq_open = nasdaq_ticker.info.get('open', '')
    nasdaq_last_close = nasdaq_ticker.info.get('previousClose', '')
    nasdaq_change = (((nasdaq_open - nasdaq_last_close) / nasdaq_last_close) * 100)
    nasdaq_change = round(nasdaq_change, 2)
    nasdaq_open = round(nasdaq_open, 2)
    nasdaq_emo = '📈' if nasdaq_change > 0 else '📉'
    body += f"\n{nasdaq_emo} {nasdaq_name}: %{nasdaq_change}"

    sp500 = "^GSPC"
    sp500_name = "S&P 500"
    sp500_ticker = yf.Ticker(sp500)
    sp500_open = sp500_ticker.info.get('open', '')
    sp500_last_close = sp500_ticker.info.get('previousClose', '')
    sp500_change = (((sp500_open - sp500_last_close) / sp500_last_close) * 100)
    sp500_change = round(sp500_change, 2)
    sp500_open = round(sp500_open, 2)
    sp500_emo = '📈' if sp500_change > 0 else '📉'
    body += f"\n{sp500_emo} {sp500_name}: %{sp500_change}"

    dowjones = "^DJI"
    dowjones_name = "Dow Jones Industrial Average"
    dowjones_ticker = yf.Ticker(dowjones)
    dowjones_open = dowjones_ticker.info.get('open', '')
    dowjones_last_close = dowjones_ticker.info.get('previousClose', '')
    dowjones_change = (((dowjones_open - dowjones_last_close) / dowjones_last_close) * 100)
    dowjones_change = round(dowjones_change, 2)
    dowjones_open = round(sp500_open, 2)
    dowjones_emo = '📈' if dowjones_change > 0 else '📉'
    body += f"\n{dowjones_emo} {dowjones_name}: %{dowjones_change}"

    body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"

    send_email(subject, body)
    # print(body)


def us_close():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day
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
        "December": "Aralık"
    }[month]
    subject = ("send_us_close #test ##test")
    body = f"""🔴 {day} {turkish_month} ABD Endeksleri Kapanış Verileri 👇

    """
    nasdaq = "^IXIC"
    nasdaq_name = "NASDAQ"
    nasdaq_data = yf.Ticker(nasdaq).history(period='max')
    nasdaq_current = nasdaq_data['Close'][-1]
    nasdaq_prev = nasdaq_data['Close'][-2]
    nasdaq_current_change = (((nasdaq_current - nasdaq_prev) / nasdaq_prev) * 100)
    nasdaq_current_change = round(nasdaq_current_change, 2)
    emo_nasdaq = '📈' if nasdaq_current_change > 0 else '📉'
    body += f"\n{emo_nasdaq} {nasdaq_name}: %{nasdaq_current_change}"

    sp500 = "^GSPC"
    sp500_name = "S&P 500"
    sp500_data = yf.Ticker(sp500).history(period='max')
    sp500_current = sp500_data['Close'][-1]
    sp500_prev = sp500_data['Close'][-2]
    sp500_current_change = (((sp500_current - sp500_prev) / sp500_prev) * 100)
    sp500_current_change = round(sp500_current_change, 2)
    emo_sp500 = '📈' if sp500_current_change > 0 else '📉'
    body += f"\n{emo_sp500} {sp500_name}: %{sp500_current_change}"

    dowjones = "^DJI"
    dowjones_name = "Dow Jones"
    dowjones_data = yf.Ticker(dowjones).history(period='max')
    dowjones_current = dowjones_data['Close'][-1]
    dowjones_prev = dowjones_data['Close'][-2]
    dowjones_current_change = (((dowjones_current - dowjones_prev) / dowjones_prev) * 100)
    dowjones_current_change = round(dowjones_current_change, 2)
    emo_dowjones = '📈' if dowjones_current_change > 0 else '📉'
    body += f"\n{emo_dowjones} {dowjones_name}: %{dowjones_current_change}"

    body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"

    send_email(subject, body)

if __name__ == "__main__":
    us_open()
    us_close()