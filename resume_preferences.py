import json
from pathlib import Path

BASE = Path(__file__).parent
PATH = BASE / "resume_preferences.json"

DEFAULTS = {
    "content_format": "Reverse-Chronological",
    "visual_theme": "Jake / Technical",
    "section_order": ["Education", "Technical Skills", "Experience", "Projects / Coursework", "Certifications", "Honors & Awards", "Leadership"],
    "include_sections": {
        "Education": True,
        "Technical Skills": True,
        "Experience": True,
        "Projects / Coursework": True,
        "Certifications": True,
        "Honors & Awards": True,
        "Leadership": True,
    },
    "emphasis": {"skills": 70, "experience": 70, "projects": 75, "coursework": 55, "credentials": 45},
    "bullet_density": "Balanced",
    "keyword_aggressiveness": "Balanced",
    "page_limit": 1,
}

CONTENT_FORMATS = ["Reverse-Chronological", "Combination / Hybrid", "Functional / Skills-Based"]
VISUAL_THEMES = [
    "Jake / Technical",
    "Modern / Contemporary",
    "Traditional / Conservative",
    "Minimal",
    "Campus / Recent Graduate",
    "Conservative Finance",
]


def load_resume_preferences():
    data = json.loads(json.dumps(DEFAULTS))
    if PATH.exists():
        try:
            loaded = json.loads(PATH.read_text(encoding="utf-8"))
            for k, v in loaded.items():
                data[k] = v
        except Exception:
            pass
    if data.get("content_format") not in CONTENT_FORMATS:
        data["content_format"] = DEFAULTS["content_format"]
    if data.get("visual_theme") not in VISUAL_THEMES:
        data["visual_theme"] = DEFAULTS["visual_theme"]
    return data


def save_resume_preferences(data):
    merged = load_resume_preferences()
    merged.update(data or {})
    PATH.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    return merged
