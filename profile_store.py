import json
import os
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
PROFILE_PATH = BASE / "candidate_profile.json"
PROFILE_ATTACHMENTS = BASE / "profile_attachments"
PROFILE_HISTORY = BASE / "profile_history"
PROFILE_ATTACHMENTS.mkdir(exist_ok=True)
PROFILE_HISTORY.mkdir(exist_ok=True)


def load_candidate_profile():
    if PROFILE_PATH.exists():
        return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    example = BASE / "candidate_profile.example.json"
    if example.exists():
        profile = json.loads(example.read_text(encoding="utf-8"))
        save_candidate_profile(profile)
        return profile
    return {"name": "", "contact": {}, "education": {}, "verified_skills": [], "target_roles": [], "certifications": [], "awards": []}


def _backup_profile():
    if not PROFILE_PATH.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    dest = PROFILE_HISTORY / f"candidate_profile_{stamp}.json"
    shutil.copy2(PROFILE_PATH, dest)
    backups = sorted(PROFILE_HISTORY.glob("candidate_profile_*.json"), reverse=True)
    for old in backups[50:]:
        old.unlink(missing_ok=True)
    return dest


def save_candidate_profile(profile):
    _backup_profile()
    tmp = PROFILE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    os.replace(tmp, PROFILE_PATH)
    return profile


def save_profile_attachment(filename, data):
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)[:120]
    path = PROFILE_ATTACHMENTS / safe
    path.write_bytes(data)
    return path
