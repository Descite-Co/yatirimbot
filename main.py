from src.crypto.crypto_utils import crypto_send
from src.etc.long_term_performance import L_term_stock
from src.bist.bist_comp import bist_comp
from src.bist.bist_sector_info import bist_sector_info
from src.bist.bist_sector_stock_info import bist_sector_stock_info
from src.bist.halka_arz import halka_arz
from src.bist.bist_30_change import bist30_change
from src.bist.bist_stock_by_time import bist_stock_by_time
from src.commodity.silver_price import silver
from src.commodity.commodity_price import commodity_price
from src.bist.bist_open_close import send_bist_open, send_bist_close
from src.etc.exchange_rates import currency_send
from src.commodity.gold_price import gold_price
from src.us.us_open_close import us_open, us_close
from app import run
from datetime import datetime
import pytz
import time


def main():
    crypto_send()
    L_term_stock()
    bist_sector_info()
    bist_comp()
    bist_sector_stock_info(datetime.now(pytz.timezone("Europe/Istanbul")).weekday())
    us_close()
    us_open()
    halka_arz()
    bist30_change()
    bist_stock_by_time()
    silver()
    commodity_price("CL=F", "Ham Petrol")  # Crude Oil
    commodity_price("HO=F", "Kalorifer Yakıtı")  # Heating Oil
    commodity_price("NG=F", "Doğal Gaz")

    # while True:
    #     tz = pytz.timezone("Europe/Istanbul")
    #     now = datetime.now(tz)

    #     if now.weekday() < 7 and now.hour == 6 and now.minute == 30:
    #         crypto_send()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 10 and now.minute == 17:
    #         send_bist_open()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 10 and now.minute == 20:
    #         halka_arz()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 10 and now.minute == 30:
    #         gold_price()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 7 and now.hour == 11 and now.minute == 00:
    #         bist_stock_by_time()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 11 and now.minute == 30:
    #         silver()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 12 and now.minute == 30:
    #         currency_send()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 13 and now.minute == 30:
    #         commodity_price("NG=F", "Doğal Gaz")
    #         time.sleep(120)
    #         continue

    #     # if now.weekday() < 5 and now.hour == 14 and now.minute == 30:
    #     #     bist_sector_info()
    #     #     time.sleep(120)
    #     #     continue

    #     if now.weekday() < 7 and now.hour == 15 and now.minute == 00:
    #         bist_stock_by_time()
    #         time.sleep(120)
    #         continue

    #     # if now.weekday() < 7 and now.hour == 15 and now.minute == 30:
    #     #     bist_sector_stock_info(now.weekday())
    #     #     time.sleep(120)
    #     #     continue

    #     if now.weekday() < 5 and now.hour == 16 and now.minute == 00:
    #         bist30_change()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 16 and now.minute == 30:
    #         gold_price()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 16 and now.minute == 46:
    #         us_open()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 7 and now.hour == 17 and now.minute == 30:
    #         L_term_stock()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 18 and now.minute == 00:
    #         crypto_send()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 18 and now.minute == 17:
    #         send_bist_close()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 19 and now.minute == 30:
    #         bist30_change()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 7 and now.hour == 19 and now.minute == 00:
    #         bist_stock_by_time()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 20 and now.minute == 00:
    #         commodity_price("CL=F", "Ham Petrol")
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 20 and now.minute == 30:
    #         bist30_change()
    #         time.sleep(120)
    #         continue

    #     # if now.weekday() < 5 and now.hour == 21 and now.minute == 30:
    #     #     bist_sector_info()
    #     #     time.sleep(120)
    #     #     continue

    #     if now.weekday() < 5 and now.hour == 22 and now.minute == 16:
    #         bist_comp()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 23 and now.minute == 16:
    #         us_close()
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 5 and now.hour == 23 and now.minute == 30:
    #         commodity_price("HO=F", "Kalorifer Yakıtı")
    #         time.sleep(120)
    #         continue

    #     if now.weekday() < 7 and now.hour == 23 and now.minute == 49:
    #         L_term_stock()
    #         time.sleep(120)
    #         continue

    #     else:
    #         time.sleep(1)
    #         continue


if __name__ == "__main__":
    main()
