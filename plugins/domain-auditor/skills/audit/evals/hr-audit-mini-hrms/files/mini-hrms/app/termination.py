from datetime import timedelta

from .leave import annual_entitlement

NOTICE_DAYS = 14


def notice_end(start):
    return start + timedelta(days=NOTICE_DAYS)


def unused_leave_compensation(emp, unused_days, avg_daily_wage):
    # bütün qalıq günlər (əsas + əlavə) kompensasiya olunur
    return unused_days * avg_daily_wage


def terminate(db, emp_id, reason, date_):
    db.execute("UPDATE employees SET termination_date=? WHERE id=?", (date_.isoformat(), emp_id))
    db.execute("INSERT INTO orders(employee_id, kind, body, created_at) VALUES (?,?,?,?)",
               (emp_id, "termination", reason, date_.isoformat()))
