import os
import json
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GMAIL_CREDENTIALS_JSON = os.getenv("GMAIL_CREDENTIALS_JSON", "")
GMAIL_TOKEN_JSON = os.getenv("GMAIL_TOKEN_JSON", "")
STATE_DB_PATH = os.getenv("STATE_DB_PATH", "state.db")
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials_dict():
    if not GMAIL_CREDENTIALS_JSON:
        return None
    try:
        return json.loads(GMAIL_CREDENTIALS_JSON)
    except json.JSONDecodeError:
        return None


def get_token_dict():
    if not GMAIL_TOKEN_JSON:
        return None
    try:
        return json.loads(GMAIL_TOKEN_JSON)
    except json.JSONDecodeError:
        return None
