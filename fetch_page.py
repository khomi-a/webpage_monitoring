# fetch_page.py
import os
import requests
import hashlib

URLS = {
    "Beachvolleyball": "https://buchung.hsp.uni-tuebingen.de/angebote/aktueller_zeitraum/_Beachvolleyball.html",
    "Volleyball": "https://buchung.hsp.uni-tuebingen.de/angebote/aktueller_zeitraum/_Volleyball.html"
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def calculate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram configuration is missing.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

def main():
    for name, url in URLS.items():
        print(f"Checking {name}...")
        content = get_page_content(url)
        new_hash = calculate_hash(content)
        
        hash_filename = f"{name.replace(' ', '_').lower()}_hash.txt"
        old_hash = ""

        if os.path.exists(hash_filename):
            with open(hash_filename, "r") as f:
                old_hash = f.read()

        if old_hash != new_hash:
            with open(hash_filename, "w") as f:
                f.write(new_hash)
            if old_hash == "":
                print(f"Initial hash saved for {name}.")
                send_telegram_message(f"⚡ Initial hash saved for {name}: {url}")
            else:
                print(f"Change detected on {name}!")
                send_telegram_message(f"⚡ Change detected on {name}: {url}")
        else:
            print(f"No changes on {name}.")

if __name__ == "__main__":
    main()