import random
from io import BytesIO

import yfinance as yf
from src.email_utils import send_email
import matplotlib.pyplot as plt


def bist_stock_by_time():
    stocks = [
        "ACSEL",
        "ADEL",
        "ADESE",
        "AEFES",
        "AFYON",
        "AGYO",
        "AKBNK",
        "AKCNS",
        "AKENR",
        "AKFGY",
        "AKGRT",
        "AKMGY",
        "AKSA",
        "AKSEN",
        "AKSGY",
        "AKSUE",
        "ALARK",
        "ALBRK",
        "ALCAR",
        "ALCTL",
        "ALGYO",
        "ALKIM",
        "ANELE",
        "ANHYT",
        "ANSGR",
        "ARCLK",
        "ARENA",
        "ARSAN",
        "ASELS",
        "ASUZU",
        "ATAGY",
        "ATEKS",
        "ATLAS",
        "ATSYH",
        "AVGYO",
        "AVHOL",
        "AVOD",
        "AVTUR",
        "AYCES",
        "AYEN",
        "AYES",
        "AYGAZ",
        "BAGFS",
        "BAKAB",
        "BALAT",
        "BANVT",
        "BASCM",
        "BEYAZ",
        "BFREN",
        "BIMAS",
        "BIZIM",
        "BJKAS",
        "BLCYT",
        "BNTAS",
        "BOSSA",
        "BRISA",
        "BRKSN",
        "BRMEN",
        "BRSAN",
        "BRYAT",
        "BSOKE",
        "BTCIM",
        "BUCIM",
        "BURCE",
        "BURVA",
        "CCOLA",
        "CELHA",
        "CEMAS",
        "CEMTS",
        "CIMSA",
        "CLEBI",
        "CMBTN",
        "CMENT",
        "COSMO",
        "CRDFA",
        "CRFSA",
        "CUSAN",
        "DAGHL",
        "DAGI",
        "DARDL",
        "DENGE",
        "DERIM",
        "DEVA",
        "DGATE",
        "DGGYO",
        "DIRIT",
        "DITAS",
        "DMSAS",
        "DOAS",
        "DOBUR",
        "DOCO",
        "DOGUB",
        "DOHOL",
        "DURDO",
        "DYOBY",
        "DZGYO",
        "ECILC",
        "ECZYT",
        "EDIP",
        "EGEEN",
        "EGGUB",
        "EGPRO",
        "EGSER",
        "EKGYO",
        "EKIZ",
        "EMKEL",
        "EMNIS",
        "ENKAI",
        "EPLAS",
        "ERBOS",
        "EREGL",
        "ERSU",
        "ESCOM",
        "ETILR",
        "ETYAT",
        "EUHOL",
        "EUKYO",
        "EUYO",
        "FENER",
        "FLAP",
        "FMIZP",
        "FRIGO",
        "FROTO",
        "GARAN",
        "GARFA",
        "GEDIK",
        "GEDZA",
        "GENTS",
        "GEREL",
        "GLBMD",
        "GLRYH",
        "GLYHO",
        "GOLTS",
        "GOODY",
        "GOZDE",
        "GRNYO",
        "GSDDE",
        "GSDHO",
        "GSRAY",
        "GUBRF",
        "HALKB",
        "HATEK",
        "HDFGS",
        "HEKTS",
        "HLGYO",
        "HURGZ",
        "ICBCT",
        "IDGYO",
        "IEYHO",
        "IHEVA",
        "IHGZT",
        "IHLAS",
        "IHYAY",
        "INDES",
        "INFO",
        "INTEM",
        "IPEKE",
        "ISBIR",
        "ISBTR",
        "ISCTR",
        "ISDMR",
        "ISFIN",
        "ISGSY",
        "ISGYO",
        "ISMEN",
        "ISYAT",
        "IZFAS",
        "IZMDC",
        "JANTS",
        "KAPLM",
        "KAREL",
        "KARSN",
        "KARTN",
        "KATMR",
        "KCHOL",
        "KENT",
        "KERVN",
        "KERVT",
        "KLGYO",
        "KLMSN",
        "KLNMA",
        "KNFRT",
        "KONYA",
        "KORDS",
        "KOZAA",
        "KOZAL",
        "KRDMA",
        "KRDMB",
        "KRDMD",
        "KRGYO",
        "KRONT",
        "KRSTL",
        "KRTEK",
        "KSTUR",
        "KUTPO",
        "KUYAS",
        "LIDFA",
        "LINK",
        "LKMNH",
        "LOGO",
        "LUKSK",
        "MAALT",
        "MAKTK",
        "MARTI",
        "MEGAP",
        "MEPET",
        "MERIT",
        "MERKO",
        "METAL",
        "METRO",
        "METUR",
        "MGROS",
        "MIPAZ",
        "MMCAS",
        "MNDRS",
        "MRGYO",
        "MRSHL",
        "MZHLD",
        "NETAS",
        "NIBAS",
        "NTHOL",
        "NUGYO",
        "NUHCM",
        "ODAS",
        "ORGE",
        "ORMA",
        "OSMEN",
        "OSTIM",
        "OTKAR",
        "OYAYO",
        "OYLUM",
        "OZGYO",
        "OZKGY",
        "OZRDN",
        "PAGYO",
        "PARSN",
        "PEGYO",
        "PENGD",
        "PETKM",
        "PETUN",
        "PGSUS",
        "PINSU",
        "PKART",
        "PKENT",
        "PNSUT",
        "POLHO",
        "POLTK",
        "PRKAB",
        "PRKME",
        "PRZMA",
        "PSDTC",
        "RAYSG",
        "RODRG",
        "RTALB",
        "RYGYO",
        "RYSAS",
        "SAHOL",
        "SAMAT",
        "SANEL",
        "SANFM",
        "SARKY",
        "SASA",
        "SAYAS",
        "SEKFK",
        "SEKUR",
        "SELEC",
        "SELGD",
        "SEYKM",
        "SILVR",
        "SISE",
        "SKBNK",
        "SKTAS",
        "SNGYO",
        "SNKRN",
        "SNPAM",
        "SODSN",
        "SONME",
        "SRVGY",
        "TATGD",
        "TAVHL",
        "TBORG",
        "TCELL",
        "TEKTU",
        "TGSAS",
        "THYAO",
        "TKFEN",
        "TKNSA",
        "TMPOL",
        "TMSN",
        "TOASO",
        "TRCAS",
        "TRGYO",
        "TSKB",
        "TSPOR",
        "TTKOM",
        "TTRAK",
        "TUCLK",
        "TUKAS",
        "TUPRS",
        "TURGG",
        "ULAS",
        "ULKER",
        "ULUSE",
        "ULUUN",
        "UMPAS",
        "USAK",
        "USAS",
        "UZERB",
        "VAKBN",
        "VAKFN",
        "VAKKO",
        "VANGD",
        "VERTU",
        "VERUS",
        "VESBE",
        "VESTL",
        "VKFYO",
        "VKGYO",
        "VKING",
        "YAPRK",
        "YATAS",
        "YAYLA",
        "YBTAS",
        "YESIL",
        "YGGYO",
        "YGYO",
        "YKBNK",
        "YONGA",
        "YUNSA",
        "YYAPI",
        "ZOREN",
    ]

    chosen_stock = random.choice(stocks)
    stock_code = chosen_stock + ".IS"
    chosen_stock_info = yf.Ticker(stock_code)

    # Retrieve historical data
    hist_data = chosen_stock_info.history(period="1y")

    # Get the latest price
    today = chosen_stock_info.info.get("currentPrice", "0")

    # Calculate percentage changes
    month_1_close = hist_data["Close"].iloc[-31]
    month_1_change_percent = (((today - month_1_close) / month_1_close) * 100).round(1)

    day_5_close = hist_data["Close"].iloc[-6]
    day_5_change_percent = (((today - day_5_close) / day_5_close) * 100).round(1)

    month_6_close = hist_data["Close"].iloc[-181]
    month_6_change_percent = (((today - month_6_close) / month_6_close) * 100).round(1)

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
    }
    month_1_day = hist_data.index[-31].strftime("%d")
    month_1_month = hist_data.index[-31].strftime("%B")
    turkish_month_1 = turkish_month[month_1_month]
    month_1_year = hist_data.index[-31].strftime("%Y")

    day_5_day = hist_data.index[-6].strftime("%d")
    day_5_year = hist_data.index[-6].strftime("%Y")
    day_5_month = hist_data.index[-6].strftime("%B")
    turkish_day_5 = turkish_month[day_5_month]

    month_6_day = hist_data.index[-181].strftime("%d")
    month_6_year = hist_data.index[-181].strftime("%Y")
    month_6_month = hist_data.index[-181].strftime("%B")
    turkish_month_6 = turkish_month[month_6_month]

    determine = lambda x: "arttı" if x > 0 else "azaldı"

    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(hist_data["Close"], label="Son Fiyat")
    plt.title(f"{chosen_stock} Hisse Senedi Grafiği")
    plt.xlabel("")
    plt.ylabel("Fiyat")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(
        image_stream, format="png"
    )  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # Construct the message
    body = f"""🔴 #{chosen_stock} Hissesinin Zamana Bağlı Performansı 👇

⬛ Güncel Fiyat: {today}
⬛ {day_5_day} {turkish_day_5} {day_5_year} tarihinden beri %{day_5_change_percent} {determine(day_5_change_percent)}.
⬛ {month_1_day} {turkish_month_1} {month_1_year} tarihinden beri %{month_1_change_percent} {determine(month_1_change_percent)}.
⬛ {month_6_day} {turkish_month_6} {month_6_year} tarihinden beri %{month_6_change_percent} {determine(month_6_change_percent)}.

          """
    subject = "bist_by_time #bist_stock_by_time"

    # print(body)
    send_email(subject, body, image_stream)


if __name__ == "__main__":
    bist_stock_by_time()
