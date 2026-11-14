import pandas as pd

from smart.category_edit import CATEGORIES, change_categories, prepare


def sample_transactions():
    return pd.DataFrame(
        {
            "date": ["2026-10-01", "2026-10-02", "2026-11-03"],
            "merchant": ["GRAB*TRIP", "SPOTIFY", "BUSINESS CENTRE"],
            "amount": [-10.0, -20.0, -30.0],
            "currency": ["MYR", "MYR", "MYR"],
        }
    )


def test_prepare_adds_category_and_marks_it_auto():
    result = prepare(sample_transactions())
    assert list(result["category"]) == ["Transport", "Subscriptions", "Other"]
    assert list(result["category_source"]) == ["auto", "auto", "auto"]


def test_prepare_keeps_categories_that_are_already_there():
    data = prepare(sample_transactions())
    data.loc[0, "category"] = "Shopping"
    data.loc[0, "category_source"] = "manual"
    result = prepare(data)
    assert result.loc[0, "category"] == "Shopping"
    assert result.loc[0, "category_source"] == "manual"


def test_prepare_does_not_change_the_original():
    original = sample_transactions()
    prepare(original)
    assert "category" not in original.columns


def test_changed_category_is_marked_manual_and_the_others_stay_auto():
    data = prepare(sample_transactions())
    edited = data.copy()
    edited.loc[1, "category"] = "Other"
    result = change_categories(data, edited)
    assert list(result["category"]) == ["Transport", "Other", "Other"]
    assert list(result["category_source"]) == ["auto", "manual", "auto"]


def test_change_categories_works_with_the_rows_of_one_month():
    data = prepare(sample_transactions())
    october = data[data["date"].str.startswith("2026-10")].copy()
    october.loc[0, "category"] = "Food"
    result = change_categories(data, october)
    assert result.loc[0, "category"] == "Food"
    assert result.loc[0, "category_source"] == "manual"
    assert result.loc[2, "category"] == "Other"
    assert result.loc[2, "category_source"] == "auto"


def test_no_change_gives_the_same_table():
    data = prepare(sample_transactions())
    result = change_categories(data, data.copy())
    assert result.equals(data)


def test_change_categories_does_not_change_the_original():
    data = prepare(sample_transactions())
    edited = data.copy()
    edited.loc[0, "category"] = "Food"
    change_categories(data, edited)
    assert data.loc[0, "category"] == "Transport"
    assert data.loc[0, "category_source"] == "auto"


def test_categories_list_has_all_categories_and_other():
    assert "Food" in CATEGORIES
    assert "Transport" in CATEGORIES
    assert CATEGORIES[-1] == "Other"
    assert len(CATEGORIES) == len(set(CATEGORIES))
