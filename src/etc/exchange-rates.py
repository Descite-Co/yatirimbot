from io import BytesIO
import requests
from matplotlib import pyplot as plt
from src.email_utils import send_email
import yfinance as yf

# TODO: Grafik çalışıyo fiyat çalışmıyo yine
def get_data_cur(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def currency_send():
    # Döviz kurlarını al
    json_data = get_data_cur('https://api.genelpara.com/embed/para-birimleri.json')

    # E-posta için içerik oluştur
    if json_data:
        email_body = "🌍 Döviz Kurları 🌍\n\n"
        for currency in ['USD', 'EUR', 'GBP']:
            data = json_data.get(currency)
            if data:
                email_body += f'#{currency}:\nFiyat: {data["satis"]}\nDeğişim: {data["degisim"]}%\n\n'
            else:
                email_body += f'{currency} verisi bulunamadı.\n\n'

        # E-posta gönder
        btc = yf.Ticker("TRY=X")
        btc_data = btc.history(period="3mo")  # adjust the period as needed

        # Plot historical prices
        plt.figure(figsize=(10, 5))
        plt.plot(btc_data['Close'], label='Son Fiyat')
        plt.title('Dolar TL 3 Aylık Grafik')
        plt.xlabel('')
        plt.ylabel('TL')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save the plot to a BytesIO buffer
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png')
        image_buffer.seek(0)

        send_email("Güncel Döviz Kurları #crypto", email_body, image_buffer)
    else:
        print("Döviz kurları alınamadı.")

if __name__ == "__main__":
    currency_send()