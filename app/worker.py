from app.gmail.reader import fetch_recent_emails
from app.processor.classifier import is_relevant, classify_email
from app.processor.extractor import format_email_data
from app.notifications.telegram import send_alert
from app.database.db import init_db, is_processed, mark_processed


def run():
    print("[INFO] Starting Internship Email Alert System...")
    init_db()

    emails = fetch_recent_emails(query="newer_than:1d", max_results=50)
    print(f"[INFO] Fetched {len(emails)} emails.")

    alerts_sent = 0
    for email_data in emails:
        message_id = email_data["message_id"]

        if is_processed(message_id):
            continue

        subject = email_data["subject"]
        body = email_data["body"]

        if not is_relevant(subject, body):
            mark_processed(message_id, "IRRELEVANT", notification_sent=False)
            continue

        classification = classify_email(subject, body)

        if classification == "REJECTED / NEGATIVE":
            mark_processed(message_id, classification, notification_sent=False)
            continue

        info = format_email_data(email_data, classification)
        sent = send_alert(
            company=info["company"],
            role=info["role"],
            status=info["status"],
            subject=info["subject"],
            received_time=info["received_time"],
            gmail_url=info["gmail_url"],
        )
        mark_processed(message_id, classification, notification_sent=sent)
        if sent:
            alerts_sent += 1
            print(f"[INFO] Alert sent for: {subject}")

    print(f"[INFO] Done. {alerts_sent} alerts sent.")


if __name__ == "__main__":
    run()
