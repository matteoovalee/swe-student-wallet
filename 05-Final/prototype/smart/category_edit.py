from smart.categorize import CATEGORY_KEYWORDS, categorize

# The categories the student can choose from when correcting a transaction.
CATEGORIES = list(CATEGORY_KEYWORDS) + ["Other"]


def prepare(transactions):
    """Return a copy of the transactions with the columns category and category_source.

    A category that is already there is kept. A missing one is set by categorize()
    and marked "auto".
    """
    result = transactions.copy()
    if "category" not in result.columns:
        result["category"] = result["merchant"].apply(categorize)
    if "category_source" not in result.columns:
        result["category_source"] = "auto"
    return result


def change_categories(transactions, edited):
    """Return a copy of transactions with the categories changed in edited.

    edited holds some of the rows of transactions (same index), for example the rows
    of one month. A row whose category is different gets the new category and is
    marked "manual". All other rows stay as they are.
    """
    result = transactions.copy()
    old_categories = result.loc[edited.index, "category"]
    changed = edited.index[edited["category"] != old_categories]
    result.loc[changed, "category"] = edited.loc[changed, "category"]
    result.loc[changed, "category_source"] = "manual"
    return result
