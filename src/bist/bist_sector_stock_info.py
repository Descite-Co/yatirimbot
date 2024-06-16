import yfinance as yf
from src.email_utils import send_email

# TODO: Error
def bist_sector_stock_info(sektor):
    stocks = {
        "Banka": ["AKBNK", "ALBRK", "GARAN", "HALKB", "ICBCT", "ISATR", "ISBTR", "ISCTR", "ISKUR", "KLNMA", "QNBFB",
                  "SKBNK", "TSKB", "VAKBN", "YKBNK"],
        "Aracı Kurum": ["A1CAP", "GEDIK", "GLBMD", "INFO", "ISMEN", "OSMEN", "OYYAT", "SKYMD", "TERA"],
        "Savunma": ["ASELS", "SDTTR"],
        "Perakende Ticaret": ["BIMAS", "BIZIM", "CASA", "CRFSA", "EBEBK", "GMTAS", "KIMMR", "MAVI", "MEPET", "MGROS",
                              "MIPAZ", "SOKM", "SUWEN", "TKNSA", "VAKKO"],
        "Bilişim": ["ALCTL", "ARDYZ", "ARENA", "ATATP", "AZTEK", "DESPC", "DGATE", "EDATA", "ESCOM", "FONET", "FORTE",
                    "HTTBT", "INDES", "INGRM", "KAREL", "KFEIN",
                    "KRONT", "LINK", "LOGO", "MANAS", "MIATK", "MOBTL", "MTRKS", "NETAS", "OBASA", "ODINE", "PAPIL",
                    "PATEK", "PENTA", "PKART", "REEDR", "SMART", "VBTYZ"],
        "Gayrimenkul Yatırım Ortaklığı": ["ADGYO", "AGYO", "AKFGY", "AKMGY", "AKSGY", "ALGYO", "ASGYO", "ATAGY",
                                          "AVGYO", "AVPGY", "BASGZ", "BEGYO", "DGGYO", "DZGYO", "EKGYO",
                                          "EYGYO", "FZLGY", "HLGYO", "IDGYO", "ISGYO", "KGYO", "KLGYO", "KRGYO",
                                          "KZBGY", "KZGYO", "MHRGY", "MRGYO", "MSGYO", "NUGYO", "OZGYO",
                                          "OZKGY", "PAGYO", "PEGYO", "PEKGY", "PSGYO", "RYGYO", "SEGYO", "SNGYO",
                                          "SRVGY", "SURGY", "TDGYO", "TRGYO", "TSGYO", "VKGYO", "VRGYO",
                                          "YGGYO", "YGYO", "ZRGYO"]
    }
    subject = ("sektor_hisse_bilgi #crypto ##crypto")
    body = f"""🔴 {sektor} Hisselerinin 5 Günlük Performansları 👇 
    \n"""
    for stock in stocks[sektor]:
        stock_code = stock + ".IS"
        stock_info = yf.Ticker(stock_code)
        stock_data = stock_info.history(period='max')
        current = stock_info.info.get('currentPrice', '0')
        day_5_close = stock_data['Close'].iloc[-6]
        day_5_change_percent = (((current - day_5_close) / day_5_close) * 100).round(1)
        emo = '📈' if day_5_change_percent > 0 else '📉'
        body += f"{emo} #{stock} {stock_info.info.get('longName', '')} %{day_5_change_percent}\n"

    #print(body)
    send_email(subject, body)

if __name__ == "__main__":
    bist_sector_stock_info("Gayrimenkul Yatırım Ortaklığı")
