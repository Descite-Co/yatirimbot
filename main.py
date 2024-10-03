"""Main script for scheduling and executing various financial tasks."""

import time
from datetime import datetime

import pytz
import schedule

from src.bist.bist_30_change import bist30_change
from src.bist.bist_comp import bist_comp
from src.bist.bist_open_close import send_bist_open, send_bist_close
from src.bist.bist_stock_by_time import bist_stock_by_time
from src.bist.halka_arz import halka_arz
from src.commodity.commodity_price import commodity_price
from src.commodity.gold_price import gold_price
from src.commodity.silver_price import analyze_silver_prices
from src.crypto.crypto_utils import crypto_send
from src.etc.exchange_rates import currency_send
from src.etc.long_term_performance import analyze_long_term_stock
from src.us.us_open_close import us_open, us_close

def is_weekday():
    """Check if the current day is a weekday."""
    return datetime.now(pytz.timezone("Europe/Istanbul")).weekday() < 5

# Daily tasks
schedule.every().day.at("06:30", "Europe/Istanbul").do(crypto_send)
schedule.every().day.at("11:00", "Europe/Istanbul").do(bist_stock_by_time)
schedule.every().day.at("15:00", "Europe/Istanbul").do(bist_stock_by_time)
schedule.every().day.at("17:30", "Europe/Istanbul").do(analyze_long_term_stock)
schedule.every().day.at("19:00", "Europe/Istanbul").do(bist_stock_by_time)
schedule.every().day.at("23:49", "Europe/Istanbul").do(analyze_long_term_stock)

# Weekday tasks
schedule.every().day.at("10:17", "Europe/Istanbul").do(send_bist_open).tag("weekday")
schedule.every().day.at("10:20", "Europe/Istanbul").do(halka_arz).tag("weekday")
schedule.every().day.at("10:30", "Europe/Istanbul").do(gold_price).tag("weekday")
schedule.every().day.at("11:30", "Europe/Istanbul").do(analyze_silver_prices).tag("weekday")
schedule.every().day.at("12:30", "Europe/Istanbul").do(currency_send).tag("weekday")
schedule.every().day.at("13:30", "Europe/Istanbul").do(lambda: commodity_price("NG=F", "Doğal Gaz")).tag("weekday")
schedule.every().day.at("16:00", "Europe/Istanbul").do(bist30_change).tag("weekday")
schedule.every().day.at("16:30", "Europe/Istanbul").do(gold_price).tag("weekday")
schedule.every().day.at("16:46", "Europe/Istanbul").do(us_open).tag("weekday")
schedule.every().day.at("18:00", "Europe/Istanbul").do(crypto_send).tag("weekday")
schedule.every().day.at("18:17", "Europe/Istanbul").do(send_bist_close).tag("weekday")
schedule.every().day.at("19:30", "Europe/Istanbul").do(bist30_change).tag("weekday")
schedule.every().day.at("20:00", "Europe/Istanbul").do(lambda: commodity_price("CL=F", "Ham Petrol")).tag("weekday")
schedule.every().day.at("20:30", "Europe/Istanbul").do(bist30_change).tag("weekday")
schedule.every().day.at("22:16", "Europe/Istanbul").do(bist_comp).tag("weekday")
schedule.every().day.at("23:16", "Europe/Istanbul").do(us_close).tag("weekday")
schedule.every().day.at("23:30", "Europe/Istanbul").do(lambda: commodity_price("HO=F", "Kalorifer Yakıtı")).tag("weekday")

def main():
    """Run the main scheduling loop."""
    # Run weekday jobs only on weekdays
    for job in schedule.get_jobs():
        if "weekday" in job.tags:
            job.run = lambda job=job: job() if is_weekday() else None

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
