from ats_engine import scan_resume
from resume_preferences import CONTENT_FORMATS, VISUAL_THEMES, load_resume_preferences
from credentials import load_catalog
from goals import load_goals


def test_goals_in_supported_range():
    g = load_goals()
    assert 2 <= g["daily_application_goal"] <= 6
    assert 2 <= g["weekly_certification_goal"] <= 6


def test_resume_preferences_have_formats_and_themes():
    p = load_resume_preferences()
    assert p["content_format"] in CONTENT_FORMATS
    assert p["visual_theme"] in VISUAL_THEMES
    assert len(VISUAL_THEMES) >= 6


def test_credential_catalog_seeded():
    items = load_catalog()["items"]
    providers = {x["provider"] for x in items}
    assert len(items) >= 20
    assert "Kaggle" in providers
    assert "Anthropic Academy" in providers
    assert "Microsoft Learn" in providers


def test_ats_scanner_is_truthful_and_bounded():
    resume = """Education
B.S. Data Science
Technical Skills
Python SQL pandas Tableau
Experience
- Analyzed customer data with Excel and SQL
- Built Tableau dashboards
"""
    jd = "Data analyst intern. Python SQL Tableau data visualization and Excel required."
    result = scan_resume(resume, jd)
    assert 0 <= result["overall"] <= 100
    assert "sql" in result["matched_skills"]
    assert "not a prediction" in result["disclaimer"]
