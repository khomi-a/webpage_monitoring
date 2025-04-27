# Page Monitor

This repository contains an automated monitoring system that checks selected web pages for changes and sends notifications via Telegram.

---

## What This Project Does

- Monitors a list of specified web pages for any content changes.
- Sends a Telegram notification if a change is detected.
- Runs automatically on a schedule using GitHub Actions.

---

## Use Cases

- Tracking schedule updates (e.g., Hochschulsport Tübingen sports programs).
- Monitoring websites for news, booking changes, price updates, and more.
- Getting real-time alerts when specific pages are updated.

---

## How to Use This for Your Own Project

1. **Fork** or clone this repository.
2. In [`fetch_page.py`](fetch_page.py), edit the `URLS` dictionary to include the pages you want to monitor.
3. In your repository settings (`Settings -> Secrets and variables -> Actions`), create two new secrets:
   - `TELEGRAM_TOKEN` — your Telegram bot token (from @BotFather).
   - `TELEGRAM_CHAT_ID` — your personal or group Chat ID in Telegram (e.g. from @userinfobot).
4. (Optional) Adjust the monitoring frequency in [`check_page.yml`](.github/workflows/check_page.yml) (by default, it runs every hour).
5. Done! GitHub Actions will automatically check the pages and notify you if anything changes. 

---

## Requirements

- A GitHub account.
- A Telegram bot (created via @BotFather).
- Your Telegram Chat ID (retrievable via bots like @userinfobot).

---

## License

Free to use, modify, and extend for your own purposes.
