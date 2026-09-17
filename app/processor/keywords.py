RELEVANCE_KEYWORDS = [
    "internship", "intern", "recruitment", "hiring", "placement",
    "interview", "assessment", "coding test", "aptitude test",
    "selection", "shortlist", "offer letter", "onboard",
    "application status", "application update", "job opening",
    "career", "opportunity", "apply now", "joining",
]

NEGATIVE_PHRASES = [
    "not selected", "unsuccessful", "rejected", "regret to inform",
    "not shortlisted", "not proceeding", "no longer under consideration",
    "decided not to move forward", "will not be moving forward",
    "unable to proceed", "position has been filled",
]

CATEGORY_KEYWORDS = {
    "SELECTED / OFFER": [
        "selected", "offer letter", "congratulations", "welcome aboard",
        "you have been selected", "pleased to offer", "offer of employment",
        "offer of internship", "selected for", "happy to inform",
    ],
    "INTERVIEW": [
        "interview", "interview invitation", "interview schedule",
        "interview details", "interview panel", "interview round",
        "schedule an interview", "interview date", "interview time",
        "technical interview", "hr interview", "behavioral interview",
    ],
    "SHORTLISTED / NEXT ROUND": [
        "shortlisted", "next round", "next stage", "proceed to",
        "moved to next round", "further evaluation", "next step",
        "advanced to", "further process",
    ],
    "ASSESSMENT / CODING TEST": [
        "assessment", "coding test", "online test", "aptitude test",
        "technical test", "test invitation", "test schedule",
        "hackerrank", "codility", "leetcode", "assessment link",
        "coding challenge", "test link",
    ],
    "INTERNSHIP OPPORTUNITY": [
        "internship opportunity", "intern opening", "intern position",
        "apply for internship", "internship program", "summer intern",
        "winter intern", "virtual intern", "internship at",
    ],
    "GENERAL RECRUITMENT": [
        "recruitment", "hiring", "job opening", "career opportunity",
        "join our team", "we are hiring", "open positions",
    ],
}

REVERSE_STATUS = {
    "selected": "SELECTED / OFFER",
    "shortlisted": "SHORTLISTED / NEXT ROUND",
    "interview": "INTERVIEW",
    "assessment": "ASSESSMENT / CODING TEST",
    "internship": "INTERNSHIP OPPORTUNITY",
    "recruitment": "GENERAL RECRUITMENT",
}
