CATEGORY_KEYWORDS = {
    "Transport": ["GRAB", "GOJEK", "TAXI", "MRT", "BUS"],
    "Food": ["FAIRPRICE", "NTUC", "FOOD", "GROCERY", "RESTAURANT"],
    "Shopping": ["SHOPEE", "LAZADA", "AMAZON", "UNIQLO"],
    "Rent": ["RENT", "LANDLORD"],
    "Subscriptions": ["SPOTIFY", "NETFLIX", "YOUTUBE", "DISNEY"],
    "Education": ["SCHOOL", "UNIVERSITY", "TUITION", "BOOKSTORE"],
    "Transfer": ["TRANSFER", "PAYNOW"],
}


def categorize(merchant):
    merchant_name = merchant.upper()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in merchant_name for keyword in keywords):
            return category

    return "Other"
