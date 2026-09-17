import base64
import email
from datetime import datetime, timezone
from app.gmail.client import get_service


def fetch_recent_emails(query="newer_than:1d", max_results=50):
    service = get_service()
    results = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        message = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()
        emails.append(parse_message(message))
    return emails


def parse_message(message):
    headers = {h["name"].lower(): h["value"] for h in message.get("payload", {}).get("headers", [])}
    body = extract_body(message.get("payload", {}))
    internal_date = int(message.get("internalDate", 0)) / 1000
    received_time = datetime.fromtimestamp(internal_date, tz=timezone.utc).isoformat()
    gmail_url = f"https://mail.google.com/mail/u/0/#inbox/{message['id']}"
    return {
        "message_id": message["id"],
        "thread_id": message.get("threadId", ""),
        "sender": headers.get("from", ""),
        "subject": headers.get("subject", ""),
        "received_time": received_time,
        "body": body,
        "gmail_url": gmail_url,
    }


def extract_body(payload):
    text = ""
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        text = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
    elif "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                text = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
                break
            elif "parts" in part:
                text = extract_body(part)
                if text:
                    break
    return text
