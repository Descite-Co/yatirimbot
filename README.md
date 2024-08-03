# Yatırım Bot | @yatirimhaberi | 2024

Yatırım Bot is a Python-based project designed to automate the sharing of financial updates and trading signals on Twitter. It provides timely information about market activities, including stock prices, commodities, and cryptocurrency updates, ensuring that users stay informed about critical financial events throughout the week.

## Table of Contents

- [Start Development Using Devbox](#start-development-using-devbox)
  - [Configure Environment Variables](#configure-environment-variables)
  - [Running the script](#running-the-script)
- [Start Development Without Devbox](#start-development-without-devbox)
  - [Install Packages](#install-packages)
  - [Configure Environment Variables](#configure-environment-variables-1)
  - [Run the main script](#run-the-main-script)
- [Çalışma Zamanları ve İşlevler](#çalışma-zamanları-ve-i̇şlevler)
  - [Hafta İçi (Pazartesi - Cuma)](#hafta-içi-pazartesi---cuma)
  - [Hafta Sonu Dahil Her Gün](#hafta-sonu-dahil-her-gün)

## Start Development Using Devbox

### Configure Environment Variables

`EMAIL`: Email of the sender

`PASSWORD`: Password for the sender SMTP

`RECEIVER`: Email for the receiver of test functions etc.

### Running the script
Install [Devbox](https://www.jetify.com/devbox/docs/installing_devbox/) if it's not already installed

Open a terminal and run the following

```bash
devbox shell
python3 main.py
```

## Start Development Without Devbox

### Install Packages
Run `pip install -r requirements.txt` to install required packages.

### Configure Environment Variables

`EMAIL`: Email of the sender

`PASSWORD`: Password for the sender SMTP

`RECEIVER`: Email for the receiver of test functions etc.

### Run the main script
Open up a terminal and run the following command

```bash
python3 main.py
```

## Çalışma Zamanları ve İşlevler

### Hafta İçi (Pazartesi - Cuma)

10:17 - BIST açılış sinyali gönderilir.

10:20 - Halka arz işlemi gerçekleştirilir.

10:30 - Altın fiyatı güncellenir.
11:30 - Gümüş fiyatı güncellenir.

12:30 - Döviz kuru güncellenir.

13:30 - Doğal Gaz fiyatı güncellenir.

16:00 ve 16:46 - BIST 30 ve ABD piyasası açılışı gerçekleştirilir.

16:30 - Altın fiyatı güncellenir.

18:17 - BIST kapanış sinyali gönderilir.

19:30 - BIST 30 değişiklikleri gerçekleştirilir.

20:00 ve 20:30 - Ham Petrol ve BIST 30 değişiklikleri gerçekleştirilir.

23:16 ve 23:30 - ABD piyasası kapanışı ve Kalorifer Yakıtı fiyatı güncellenir.

### Hafta Sonu Dahil Her Gün

06:30 ve 18:00 - Kripto para birimi güncellemeleri gönderilir.

11:00, 15:00 ve 19:00 - BIST hisse senedi zamanına göre işlemler yapılır.

17:30 ve 23:49 - Uzun vadeli hisse senetleri güncellenir.
