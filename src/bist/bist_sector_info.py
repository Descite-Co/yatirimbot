from datetime import datetime;
import pytz
import yfinance as yf
from src.email_utils import send_email

# TODO: Sadece #XUSIN, #XBANK çalışıyor
def bist_sector_info(start, end):
    tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(tz)
    endeksler = ["XUSIN", "XUHIZ", "XUMAL", "XUTEK", "XBANK", "XAKUR", "XBLSM", "XELKT", "XFINK", "XGMYO", "XGIDA",
                 "XHOLD",
                 "XILTM", "XINSA", "XKAGT", "XKMYA", "XMADN", "XYORT", "XMANA", "XMESY", "XSGRT", "XSPOR", "XTAST",
                 "XTEKS",
                 "XTCRT", "XTRZM", "XULAS"]
    endeksler = endeksler[start:end + 1]
    subject = "sektor_hisse_bilgi"
    body = "🔴 Borsa İstanbul Endekslerinin 5 Günlük Performansları 👇\n"

    for index in endeksler:
        try:
            stock_code = index + ".IS"
            endeks = yf.Ticker(stock_code)
            endeks_data = endeks.history(period='5d')
            if len(endeks_data) >= 5:
                current = endeks_data['Close'].iloc[-1]
                day5 = endeks_data['Close'].iloc[-5]
                change = (((current - day5) / day5) * 100)
                change = round(change, 2)
                text = 'Yükseldi' if change > 0 else 'Düştü'
                emo = '📈' if change > 0 else '📉'
                body += f"{emo} #{index} {endeks.info.get('longName', 'Bilgi Yok')} 5 Günde %{change} {text}\n"
            else:
                body += f"🔍 #{index} Yeterli veri yok\n"
        except Exception as e:
            body += f"⚠️ #{index} Veri alınırken hata: {str(e)}\n"

    #print(body)
    send_email(subject, body)


if __name__ == "__main__":
    bist_sector_info(0, 26)