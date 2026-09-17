import json
import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from app.config import SCOPES, GMAIL_CREDENTIALS_JSON, GMAIL_TOKEN_JSON


TOKEN_PATH = "token.json"


def _fail(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def authenticate_local():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not GMAIL_CREDENTIALS_JSON:
                _fail(
                    "GMAIL_CREDENTIALS_JSON not set.\n"
                    "  1. Go to https://console.cloud.google.com/\n"
                    "  2. Create OAuth 2.0 Client ID (Desktop app)\n"
                    "  3. Download credentials.json\n"
                    "  4. Set GMAIL_CREDENTIALS_JSON env var to the file contents\n"
                    "  Or place credentials.json in the project root."
                )
            creds_dict = json.loads(GMAIL_CREDENTIALS_JSON)
            with open("credentials.json", "w") as f:
                json.dump(creds_dict, f)
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            os.remove("credentials.json")
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


def authenticate_production():
    if not GMAIL_CREDENTIALS_JSON:
        _fail("GMAIL_CREDENTIALS_JSON not set.")
    if not GMAIL_TOKEN_JSON:
        _fail("GMAIL_TOKEN_JSON not set. Run locally first to generate token.json.")
    creds_dict = json.loads(GMAIL_CREDENTIALS_JSON)
    token_dict = json.loads(GMAIL_TOKEN_JSON)

    missing = []
    if not token_dict.get("refresh_token"):
        missing.append("refresh_token (in GMAIL_TOKEN_JSON)")
    if not token_dict.get("token"):
        missing.append("token (in GMAIL_TOKEN_JSON)")
    if not creds_dict.get("client_id"):
        missing.append("client_id (in GMAIL_CREDENTIALS_JSON)")
    if not creds_dict.get("client_secret"):
        missing.append("client_secret (in GMAIL_CREDENTIALS_JSON)")
    if not creds_dict.get("token_uri"):
        missing.append("token_uri (in GMAIL_CREDENTIALS_JSON)")
    if missing:
        _fail(
            "Missing required fields:\n  "
            + "\n  ".join(missing)
            + "\n\nMake sure GMAIL_CREDENTIALS_JSON has: client_id, client_secret, token_uri"
            "\nMake sure GMAIL_TOKEN_JSON has: token, refresh_token"
            "\nCopy the FULL file contents of credentials.json and token.json."
        )

    creds = Credentials(
        token=token_dict.get("token"),
        refresh_token=token_dict.get("refresh_token"),
        token_uri=creds_dict.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=creds_dict.get("client_id"),
        client_secret=creds_dict.get("client_secret"),
        scopes=SCOPES,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds


def get_gmail_service():
    if GMAIL_TOKEN_JSON:
        return authenticate_production()
    if GMAIL_CREDENTIALS_JSON:
        creds_dict = json.loads(GMAIL_CREDENTIALS_JSON)
        if "installed" in creds_dict or "web" in creds_dict:
            return authenticate_local()
    _fail(
        "No Gmail credentials found.\n"
        "  Set GMAIL_CREDENTIALS_JSON or GMAIL_TOKEN_JSON env var.\n"
        "  See README.md for setup instructions."
    )
