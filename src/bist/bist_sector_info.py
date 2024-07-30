from datetime import datetime;
import pytz
import yfinance as yf
from src.email_utils import send_email
import random

def bist_sector_info():
    tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(tz)
    endeksler = ["XUSIN", "XUHIZ", "XUMAL", "XUTEK", "XBANK", "XAKUR", "XBLSM", "XELKT", "XFINK", "XGMYO", "XGIDA",
                 "XHOLD", "XILTM", "XINSA", "XKAGT", "XKMYA", "XMADN", "XYORT", "XMANA", "XMESY", "XSGRT", "XSPOR",
                 "XTAST", "XTEKS", "XTCRT", "XTRZM", "XULAS"]
    random_sectors = random.sample(endeksler, 5)
    subject = "sektor_hisse_bilgi"
    body = "🔴 Borsa İstanbul Endekslerinin Bugünkü Performansları 👇\n"

    for index in random_sectors:
        try:
            stock_code = index + ".IS"
            endeks = yf.Ticker(stock_code)
            endeks_data = endeks.history(period='1d')

            if len(endeks_data) >= 1:
                current = endeks_data['Close'].iloc[-1]
                open_price = endeks_data['Open'].iloc[-1]
                change = (((current - open_price) / open_price) * 100)
                change = round(change, 2)
                text = 'Yükseldi' if change > 0 else 'Düştü'
                emo = '📈' if change > 0 else '📉'
                body += f"{emo} #{index} {endeks.info.get('longName', 'Bilgi Yok')} %{change} {text}\n"
            else:
                body += f"🔍 #{index} Yeterli veri yok\n"
        except Exception as e:
            body += f"⚠️ #{index} Veri alınırken hata: {str(e)}\n"

    #print(body)
    send_email(subject, body)


if __name__ == "__main__":
    bist_sector_info(0, 26)