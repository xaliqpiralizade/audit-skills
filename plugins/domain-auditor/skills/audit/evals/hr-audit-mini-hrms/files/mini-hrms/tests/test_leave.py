from datetime import date

from app.leave import annual_entitlement, leave_length


def test_base():
    assert annual_entitlement({"hire_date": date(2024, 1, 1)}, date(2024, 6, 1)) == 18


def test_length_skips_weekend():
    assert leave_length(date(2024, 7, 1), date(2024, 7, 14)) == 10
