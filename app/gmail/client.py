from googleapiclient.discovery import build
from app.gmail.auth import get_gmail_service


def get_service():
    creds = get_gmail_service()
    return build("gmail", "v1", credentials=creds)
