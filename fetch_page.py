import os
import requests
import hashlib
from bs4 import BeautifulSoup

# Список страниц для отслеживания
URLS = {
    "Beachvolleyball": "https://buchung.hsp.uni-tuebingen.de/angebote/aktueller_zeitraum/_Beachvolleyball.html",
    "Volleyball": "https://buchung.hsp.uni-tuebingen.de/angebote/aktueller_zeitraum/_Volleyball.html"
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram configuration is missing.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

def get_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def check_slots(html):
    soup = BeautifulSoup(html, 'html.parser')
    alerts = []
    rows = soup.find_all('tr', class_='bs_even') + soup.find_all('tr', class_='bs_odd')

    for row in rows:
        detail_cell = row.find('td', class_='bs_sdet')
        if not detail_cell:
            continue
        detail_text = detail_cell.get_text(strip=True)

        if detail_text not in ('Fortg. Mixed', 'Freies Spiel Fortg'):
            continue

        booking_cell = row.find('td', class_='bs_sbuch')
        if not booking_cell:
            continue
        button = booking_cell.find('input', {'type': 'submit'})

        if not button:
            continue

        button_class = button.get('class', [''])[0] if button.has_attr('class') else ''

        if button_class not in ('bs_btn_warteliste', 'bs_btn_ausgebucht'):
            kurs_id = row.get('id', 'unknown')
            alerts.append(f"📢 Slot available: {detail_text} ({kurs_id}) → {button.get('value', '')}")

    return alerts

def main():
    for name, url in URLS.items():
        print(f"Checking {name}...")
        html = get_page_content(url)
        alerts = check_slots(html)

        if alerts:
            for msg in alerts:
                send_telegram_message(msg)
        else:
            print(f"No open slots found for {name}.")

if __name__ == "__main__":
    main()