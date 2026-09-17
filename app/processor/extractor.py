import re


def extract_company(sender, subject, body):
    company = extract_company_from_sender(sender)
    if company:
        return company
    company = extract_company_from_subject(subject)
    if company:
        return company
    return "Unknown"


def extract_company_from_sender(sender):
    match = re.search(r"@([\w.-]+)", sender)
    if match:
        domain = match.group(1)
        domain = domain.split(".")[0]
        if domain.lower() not in ("gmail", "yahoo", "outlook", "hotmail", "rediffmail"):
            return domain.capitalize()
    return None


def extract_company_from_subject(subject):
    patterns = [
        r"(?:from|at|@)\s+([A-Z][\w\s&]+)",
        r"^([A-Z][\w\s&]+)\s*[-:|]",
        r"\b([A-Z][\w]+)\s+(?:Internship|Interview|Assessment|Hiring|Recruitment)",
    ]
    for pattern in patterns:
        match = re.search(pattern, subject)
        if match:
            return match.group(1).strip()
    return None


def extract_role(subject, body):
    text = subject + " " + body
    patterns = [
        r"(?:role|position|profile|designation)[:\s]+([^\n,]+)",
        r"(?:for|as)\s+(?:a\s+)?([^\n,]+?(?:intern|engineer|developer|analyst|internship)[^\n,]*)",
        r"([A-Z][\w\s]+?(?:Internship|Intern|Position|Role))\b",
        r"([A-Z][\w\s]+?)(?:\s+Internship|\s+Intern\b)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            role = match.group(1).strip()
            if 3 < len(role) < 60:
                return role
    return "Unknown"


def extract_status(classification):
    status_map = {
        "SELECTED / OFFER": "Selected / Offer",
        "SHORTLISTED / NEXT ROUND": "Shortlisted / Next Round",
        "INTERVIEW": "Interview",
        "ASSESSMENT / CODING TEST": "Assessment / Coding Test",
        "INTERNSHIP OPPORTUNITY": "Internship Opportunity",
        "GENERAL RECRUITMENT": "General Recruitment",
        "REJECTED / NEGATIVE": "Rejected / Negative",
    }
    return status_map.get(classification, classification)


def format_email_data(email_data, classification):
    company = extract_company(email_data["sender"], email_data["subject"], email_data["body"])
    role = extract_role(email_data["subject"], email_data["body"])
    status = extract_status(classification)
    return {
        "company": company,
        "role": role,
        "status": status,
        "subject": email_data["subject"],
        "received_time": email_data["received_time"],
        "gmail_url": email_data["gmail_url"],
    }
