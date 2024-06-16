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
from app import run

def main():
    crypto_send()
    L_term_stock()
    bist_sector_info(0, 26)
    bist_comp()
    bist_sector_stock_info("Gayrimenkul Yatırım Ortaklığı")
    halka_arz()
    bist30_change()
    bist_stock_by_time()
    silver()
    commodity_price('CL=F', 'Ham Petrol')  # Crude Oil
    commodity_price('HO=F', 'Kalorifer Yakıtı')  # Heating Oil
    commodity_price('NG=F', 'Doğal Gaz')


if __name__ == "__main__":
    main()
