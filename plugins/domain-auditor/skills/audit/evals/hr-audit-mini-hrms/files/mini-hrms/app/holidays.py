from datetime import date

# Azərbaycanın bayram günləri
HOLIDAYS = [
    date(2024, 1, 1), date(2024, 1, 2),
    date(2024, 3, 8),
    date(2024, 3, 20), date(2024, 3, 21), date(2024, 3, 22), date(2024, 3, 23), date(2024, 3, 24),  # Novruz
    date(2024, 4, 10), date(2024, 4, 11),   # Ramazan
    date(2024, 5, 9), date(2024, 5, 28),
    date(2024, 6, 15), date(2024, 6, 16), date(2024, 6, 17),  # Qurban
    date(2024, 6, 26),
    date(2024, 11, 8), date(2024, 11, 9),
    date(2024, 12, 31),
]


def is_holiday(d):
    return d in HOLIDAYS
