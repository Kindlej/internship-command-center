import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
SETTINGS = BASE / "goal_settings.json"
DB = BASE / "applications.db"

DEFAULTS = {
    "daily_application_goal": 3,
    "weekly_certification_goal": 2,
    "application_streak_enabled": True,
    "credential_streak_enabled": True,
}


def load_goals():
    data = dict(DEFAULTS)
    if SETTINGS.exists():
        try:
            data.update(json.loads(SETTINGS.read_text(encoding="utf-8")))
        except Exception:
            pass
    data["daily_application_goal"] = max(2, min(6, int(data.get("daily_application_goal", 3))))
    data["weekly_certification_goal"] = max(2, min(6, int(data.get("weekly_certification_goal", 2))))
    return data


def save_goals(data):
    clean = dict(DEFAULTS)
    clean.update(data or {})
    clean["daily_application_goal"] = max(2, min(6, int(clean["daily_application_goal"])))
    clean["weekly_certification_goal"] = max(2, min(6, int(clean["weekly_certification_goal"])))
    SETTINGS.write_text(json.dumps(clean, indent=2), encoding="utf-8")
    return clean


def _con():
    return sqlite3.connect(DB)


def applications_submitted_today():
    if not DB.exists():
        return 0
    con = _con()
    try:
        row = con.execute(
            """SELECT COUNT(*) FROM opportunities
               WHERE submitted_at IS NOT NULL
               AND date(submitted_at, 'localtime') = date('now', 'localtime')"""
        ).fetchone()
        return int(row[0] or 0)
    except Exception:
        return 0
    finally:
        con.close()


def applications_submitted_on(date_obj):
    if not DB.exists():
        return 0
    con = _con()
    try:
        row = con.execute(
            """SELECT COUNT(*) FROM opportunities
               WHERE submitted_at IS NOT NULL AND date(submitted_at)=?""",
            (date_obj.isoformat(),),
        ).fetchone()
        return int(row[0] or 0)
    except Exception:
        return 0
    finally:
        con.close()


def application_streak(goal=None, max_days=365):
    goal = int(goal or load_goals()["daily_application_goal"])
    today = datetime.now().date()
    streak = 0
    for offset in range(max_days):
        d = today - timedelta(days=offset)
        count = applications_submitted_on(d)
        if offset == 0 and count < goal:
            # An unfinished current day should not erase yesterday's completed streak.
            continue
        if count >= goal:
            streak += 1
        else:
            break
    return streak
