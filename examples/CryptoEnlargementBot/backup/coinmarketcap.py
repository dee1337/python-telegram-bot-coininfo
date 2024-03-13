#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      dee1337
#
# Created:     11.03.2024
# Copyright:   (c) dee1337 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup
import time

# URL für die Bitcoin-Seite auf CoinMarketCap
URL = 'https://coinmarketcap.com/currencies/'

# Funktion zum Abrufen des aktuellen Bitcoin-ATH von der Webseite
def get_bitcoin_ath_date():
    # datum regex: r"^\w\w\w\s..\,\s\d{4} => Mar 11, 2024
    response = requests.get(URL+'bitcoin')
    soup = BeautifulSoup(response.text, 'html.parser')
    # Finden des Elements, das den ATH-Preis enthält
    ath_element = soup.find('div', class_='sc-f70bb44c-0 iQEJet text').text
    ath_date = ath_element
    return ath_date

# Funktion zum Abrufen des aktuellen Bitcoin-ATH von der Webseite
def get_bitcoin_ath():
    response = requests.get(URL+'bitcoin')
    soup = BeautifulSoup(response.text, 'html.parser')
    # Finden des Elements, das den ATH-Preis enthält
    ath_element = soup.find('div', class_='sc-f70bb44c-0 dVdjLB')
    ath_price = ath_element.find('span').text
    ath_date = get_bitcoin_ath_date()
    # $-Zeichen entfernen
    return float(ath_price[1:].replace(',', ''))


def ath_tracker(update_rate = 60):
    # Variable zum Speichern des zuletzt gespeicherten ATH-Preises
    last_ath = get_bitcoin_ath()

    # Schleife für die periodische Überprüfung
    while True:
        current_ath = get_bitcoin_ath()
        # Überprüfen, ob sich der ATH-Preis geändert hat
        if current_ath != last_ath:
            ath_date = get_bitcoin_ath_date()
            last_ath = current_ath
            print(f'Bitcoin ATH hat sich geändert! Neuer ATH: ${current_ath}')

            print(f'Bitcoin ATH hat sich geändert am {ath_date}')
        else:
            print('Bitcoin ATH hat sich nicht geändert.')

        # Wartezeit für 1 Minute
        time.sleep(update_rate)  # jede Minute mal schauen


