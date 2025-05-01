import os
import re
import requests
from html import unescape

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

def check_slots(html):
    alerts = []

    # Извлекаем все блоки <tr>...</tr>
    rows = re.findall(r"<tr.*?</tr>", html, flags=re.DOTALL)

    for row in rows:
        # Получаем kurs_id из id атрибута <tr>
        id_match = re.search(r'<tr[^>]*id=["\']([^"\']+)["\']', row)
        kurs_id = id_match.group(1) if id_match else "unknown"

        # Извлекаем название курса
        sdet_match = re.search(r"<td class=['\"]bs_sdet['\"]>(.*?)</td>", row, flags=re.DOTALL)
        if not sdet_match:
            continue

        detail_text = unescape(re.sub(r"<.*?>", "", sdet_match.group(1))).strip()
        if detail_text not in ("Fortg. Mixed", "Freies Spiel Fortg"):
            continue

        # Извлекаем input-кнопку
        button_match = re.search(r'<input[^>]+class=["\']([^"\']+)["\'][^>]+value=["\']([^"\']+)["\']', row)
        if not button_match:
            continue

        button_class = button_match.group(1)
        button_value = button_match.group(2)

        if button_class not in ('bs_btn_warteliste', 'bs_btn_ausgebucht'):
            alerts.append(f"📢 Slot available: {detail_text} ({kurs_id}) → {button_value}")

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

def get_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    main()
