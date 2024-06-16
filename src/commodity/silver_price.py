from io import BytesIO
import requests
from matplotlib import pyplot as plt
from src.email_utils import send_email
import yfinance as yf

# TODO: Grafik çalışıyo fiyat çalışmıyo

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

def silver():
    # Gümüş verilerini al
    json_data = get_data_cur('https://api.genelpara.com/embed/para-birimleri.json')

    # E-posta için içerik oluştur
    if json_data:
        data = json_data.get('GAG')
        if data:
            email_body = "🔴 #Gümüş:\n"
            email_body += f'Fiyat: ₺{data["satis"]}\nDeğişim: {data["degisim"]}%\n'

            silver = yf.Ticker('SI=F')
            hist_data = silver.history(period='max')

            # Plot historical prices
            plt.figure(figsize=(12, 6))
            plt.plot(hist_data['Close'], label='Son Fiyat')
            plt.title('Gümüş Dolar Grafiği')
            plt.xlabel('')
            plt.ylabel('Fiyat')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the plot as a BytesIO object
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
            image_stream.seek(0)

            # E-posta gönder
            send_email("Güncel Gümüş Fiyatları #crypto", email_body, image_stream)
            #print(email_body)

        else:
            print('Gümüş verisi bulunamadı.')
    else:
        print("Veri alınamadı.")

if __name__ == "__main__":
    silver()