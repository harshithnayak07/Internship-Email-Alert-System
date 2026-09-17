import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app.processor.classifier import is_relevant, classify_email, is_negative
from app.processor.extractor import extract_company, extract_role, extract_status, format_email_data
from app.database.db import init_db, is_processed, mark_processed


@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    os.environ["STATE_DB_PATH"] = str(tmp_path / "test.db")
    from app import config
    config.STATE_DB_PATH = str(tmp_path / "test.db")
    init_db()
    yield


class TestClassification:
    def test_internship_opportunity(self):
        subject = "Summer Internship Opportunity at Google"
        body = "We are looking for software engineering interns."
        assert classify_email(subject, body) == "INTERNSHIP OPPORTUNITY"

    def test_interview(self):
        subject = "Interview Invitation - Python Developer Role"
        body = "You have been shortlisted for a technical interview."
        assert classify_email(subject, body) == "INTERVIEW"

    def test_assessment(self):
        subject = "Online Assessment - Coding Test"
        body = "Please complete the assessment link below."
        assert classify_email(subject, body) == "ASSESSMENT / CODING TEST"

    def test_selected_offer(self):
        subject = "Congratulations! You have been selected"
        body = "We are pleased to offer you the internship position."
        assert classify_email(subject, body) == "SELECTED / OFFER"

    def test_shortlisted(self):
        subject = "Application Update - Shortlisted for next round"
        body = "You have been shortlisted for the next round."
        assert classify_email(subject, body) == "SHORTLISTED / NEXT ROUND"

    def test_general_recruitment(self):
        subject = "We are hiring - Join our team"
        body = "Check out our open positions."
        assert classify_email(subject, body) == "GENERAL RECRUITMENT"

    def test_rejection_not_selected(self):
        subject = "Application Status Update"
        body = "We regret to inform you that you were not selected."
        assert classify_email(subject, body) == "REJECTED / NEGATIVE"

    def test_rejection_unsuccessful(self):
        subject = "Interview Result"
        body = "Your application was unsuccessful."
        assert classify_email(subject, body) == "REJECTED / NEGATIVE"

    def test_rejection_rejected(self):
        subject = "Application Update"
        body = "We regret to inform you that your application has been rejected."
        assert classify_email(subject, body) == "REJECTED / NEGATIVE"

    def test_rejection_not_shortlisted(self):
        subject = "Application Status"
        body = "We are sorry to inform you that you are not shortlisted."
        assert classify_email(subject, body) == "REJECTED / NEGATIVE"

    def test_negative_detection(self):
        assert is_negative("Status", "We regret to inform you that you were not selected")
        assert is_negative("Update", "Your application was unsuccessful")
        assert not is_negative("Invitation", "You are invited for an interview")


class TestRelevance:
    def test_relevant_internship(self):
        assert is_relevant("Internship at Microsoft", "Apply for software intern role")

    def test_relevant_interview(self):
        assert is_relevant("Interview Schedule", "Your interview is on Monday")

    def test_unrelated_email(self):
        assert not is_relevant("Weekly Newsletter", "Here are the top stories this week")

    def test_rejected_not_relevant(self):
        assert not is_relevant("Application Update", "We regret to inform you that you were not selected")

    def test_relevant_assessment(self):
        assert is_relevant("Online Test", "Please complete the coding test")


class TestExtraction:
    def test_company_from_sender(self):
        assert extract_company("careers@google.com", "", "") == "Google"

    def test_company_from_sender_unknown(self):
        assert extract_company("user@gmail.com", "", "") == "Unknown"

    def test_company_from_sender_microsoft(self):
        assert extract_company("hr@microsoft.com", "", "") == "Microsoft"

    def test_role_intern(self):
        role = extract_role("Python Developer Internship", "")
        assert "intern" in role.lower() or role == "Unknown"

    def test_role_from_subject(self):
        role = extract_role("Hiring: Software Engineer", "")
        assert role != ""

    def test_status_mapping(self):
        assert extract_status("SELECTED / OFFER") == "Selected / Offer"
        assert extract_status("INTERVIEW") == "Interview"
        assert extract_status("ASSESSMENT / CODING TEST") == "Assessment / Coding Test"
        assert extract_status("INTERNSHIP OPPORTUNITY") == "Internship Opportunity"
        assert extract_status("REJECTED / NEGATIVE") == "Rejected / Negative"


class TestFormatEmailData:
    def test_format(self):
        email_data = {
            "sender": "hr@techcorp.com",
            "subject": "Interview Invitation - Python Intern",
            "body": "You have been shortlisted for an interview.",
            "received_time": "2025-01-01T00:00:00",
            "gmail_url": "https://mail.google.com/mail/u/0/#inbox/abc123",
        }
        result = format_email_data(email_data, "INTERVIEW")
        assert result["company"] == "Techcorp"
        assert result["status"] == "Interview"
        assert "Python" in result["subject"]


class TestDuplicatePrevention:
    def test_mark_and_check(self):
        assert not is_processed("msg_001")
        mark_processed("msg_001", "INTERVIEW", notification_sent=True)
        assert is_processed("msg_001")

    def test_different_messages(self):
        mark_processed("msg_001", "INTERVIEW")
        mark_processed("msg_002", "ASSESSMENT / CODING TEST")
        assert is_processed("msg_001")
        assert is_processed("msg_002")
        assert not is_processed("msg_003")
