from datetime import datetime;
import pytz
import yfinance as yf
from src.email_utils import send_email

def halka_arz():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day  # BUNU HER DAY KULLANILAN YERDE KULLANALIM
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
    stocks = ['RGYAS', 'ODINE', 'MOGAN', 'ARTMS', 'ALVES', 'LMKDC']
    change_rates = []
    stock_prices = []
    subject = ("halka_arz_tablosu #test ##test")
    body = f"""🔴 {day} {turkish_month} Halka Arz Tablosu \n
"""
    for stock in stocks[::-1]:
        stock_code = stock + '.IS'
        hisse = yf.Ticker(stock_code)
        hisse_data = hisse.history(period='max')
        hisse_close_list = hisse_data['Close'][-3:].tolist()
        print(hisse_close_list)
        hisse_current = hisse_close_list[2]
        hisse_prev = hisse_close_list[1]
        hisse_current_change = (((hisse_current - hisse_prev) / hisse_prev) * 100)
        hisse_current_change = round(hisse_current_change, 2)
        change_rates.append(hisse_current_change)
        stock_prices.append(hisse_current)
        emo = '📈' if hisse_current_change > 0 else '📉'
        text = 'yükseldi' if hisse_current_change > 0 else 'düştü'
        tavan_check = " - Hisse Tavanda" if hisse_current_change > 9.5 else ""
        message = f"{emo} #{stock} bugün %{hisse_current_change} {text}"
        body += f"{message + tavan_check}\n"
    send_email(subject, body)

if __name__ == "__main__":
    halka_arz();