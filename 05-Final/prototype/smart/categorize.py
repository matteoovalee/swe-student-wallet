import re

CATEGORY_KEYWORDS = {
    "Transport": [
        "GRAB",
        "GOJEK",
        "TAXI",
        "MRT",
        "BUS",
        "RAPID KL",
        "TOUCH N GO",
    ],
    "Food": [
        "FAIRPRICE",
        "NTUC",
        "FOOD",
        "GROCERY",
        "RESTAURANT",
        "MCDONALDS",
        "LOTUS'S",
        "FAMILYMART",
        "CAMPUS CAFE",
        "TEALIVE",
        "MYDIN",
        "7-ELEVEN",
    ],
    "Shopping": ["SHOPEE", "LAZADA", "AMAZON", "UNIQLO"],
    "Rent": ["RENT", "LANDLORD"],
    "Subscriptions": [
        "SPOTIFY",
        "NETFLIX",
        "YOUTUBE",
        "DISNEY",
        "PHONE DATA PLAN",
    ],
    "Education": [
        "SCHOOL",
        "UNIVERSITY",
        "TUITION",
        "BOOKSTORE",
        "PRINT SHOP",
    ],
    "Transfer": ["TRANSFER", "PAYNOW"],
}


def _has_keyword(keyword, merchant_name):
    # whole-word match: "RENT" must not match "CURRENT", "BUS" must not match "BUSINESS"
    return re.search(rf"\b{re.escape(keyword)}\b", merchant_name) is not None


def categorize(merchant):
    if not isinstance(merchant, str):
        return "Other"

    merchant_name = merchant.upper()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(_has_keyword(keyword, merchant_name) for keyword in keywords):
            return category

    return "Other"
