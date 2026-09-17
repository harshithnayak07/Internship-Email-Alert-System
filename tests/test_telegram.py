import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from unittest.mock import patch, MagicMock
from app.notifications.telegram import send_alert


class TestTelegram:
    @patch("app.notifications.telegram.TELEGRAM_CHAT_ID", "12345")
    @patch("app.notifications.telegram.TELEGRAM_BOT_TOKEN", "test_token")
    @patch("app.notifications.telegram.requests.post")
    def test_send_alert_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = send_alert(
            company="Google",
            role="Python Intern",
            status="Interview",
            subject="Interview Invitation",
            received_time="2025-01-01T00:00:00",
            gmail_url="https://mail.google.com/mail/u/0/#inbox/abc",
        )
        assert result is True
        mock_post.assert_called_once()

    @patch("app.notifications.telegram.TELEGRAM_CHAT_ID", "12345")
    @patch("app.notifications.telegram.TELEGRAM_BOT_TOKEN", "test_token")
    @patch("app.notifications.telegram.requests.post")
    def test_send_alert_failure(self, mock_post):
        import requests
        mock_post.side_effect = requests.RequestException("Timeout")

        result = send_alert(
            company="Google",
            role="Python Intern",
            status="Interview",
            subject="Interview Invitation",
            received_time="2025-01-01T00:00:00",
            gmail_url="https://mail.google.com/mail/u/0/#inbox/abc",
        )
        assert result is False

    @patch("app.notifications.telegram.TELEGRAM_CHAT_ID", "")
    @patch("app.notifications.telegram.TELEGRAM_BOT_TOKEN", "")
    @patch("app.notifications.telegram.requests.post")
    def test_send_alert_no_credentials(self, mock_post):
        result = send_alert(
            company="Google",
            role="Python Intern",
            status="Interview",
            subject="Interview Invitation",
            received_time="2025-01-01T00:00:00",
            gmail_url="https://mail.google.com/mail/u/0/#inbox/abc",
        )
        assert result is False
        mock_post.assert_not_called()
