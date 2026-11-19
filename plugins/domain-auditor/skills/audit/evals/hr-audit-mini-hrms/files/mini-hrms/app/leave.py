from datetime import date, timedelta

from .holidays import is_holiday

BASE_DAYS = 18  # illik əsas məzuniyyət


def seniority_years(hire_date, today=None):
    today = today or date.today()
    return today.year - hire_date.year


def extra_days_for_seniority(years):
    if years >= 10:
        return 4
    if years >= 3:
        return 2
    return 0


def annual_entitlement(emp, today=None):
    days = BASE_DAYS
    days += extra_days_for_seniority(seniority_years(emp["hire_date"], today))
    return days


def leave_length(start, end):
    """Məzuniyyət günlərinin sayı (iş günləri)."""
    d, n = start, 0
    while d <= end:
        if d.weekday() < 5 and not is_holiday(d):
            n += 1
        d += timedelta(days=1)
    return n


def remaining_balance(emp, leaves, today=None):
    today = today or date.today()
    used = sum(l["days"] for l in leaves if l["start_date"].year == today.year and l["type"] == "annual")
    return annual_entitlement(emp, today) - used


def can_take_leave(emp, today=None):
    return True
