from app.processor.keywords import RELEVANCE_KEYWORDS, NEGATIVE_PHRASES, CATEGORY_KEYWORDS


def is_relevant(subject, body):
    text = (subject + " " + body).lower()
    for phrase in NEGATIVE_PHRASES:
        if phrase in text:
            return False
    for kw in RELEVANCE_KEYWORDS:
        if kw in text:
            return True
    return False


def classify_email(subject, body):
    text = (subject + " " + body).lower()
    for phrase in NEGATIVE_PHRASES:
        if phrase in text:
            return "REJECTED / NEGATIVE"
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category
    return "GENERAL RECRUITMENT"


def is_negative(subject, body):
    text = (subject + " " + body).lower()
    for phrase in NEGATIVE_PHRASES:
        if phrase in text:
            return True
    return False
