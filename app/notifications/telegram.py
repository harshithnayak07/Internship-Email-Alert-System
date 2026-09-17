import requests
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_alert(company, role, status, subject, received_time, gmail_url):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARN] Telegram credentials not set. Skipping notification.")
        return False

    message = (
        "🚨 *Internship Alert*\n\n"
        f"*Status:* {status}\n"
        f"*Company:* {company}\n"
        f"*Role:* {role}\n"
        f"*Subject:* {subject}\n"
        f"*Received:* {received_time}\n\n"
        f"[Open Email]({gmail_url})"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[ERROR] Telegram send failed: {e}")
        return False
