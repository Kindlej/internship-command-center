import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "credentials.json"
EVIDENCE = BASE / "credential_evidence"
CATALOG = BASE / "credential_catalog.json"


def _load(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def load_credentials():
    return _load(DATA, {"items": []})


def save_credentials(data):
    DATA.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_catalog():
    return _load(CATALOG, {"items": []})


def save_evidence(uploaded_file):
    EVIDENCE.mkdir(exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in uploaded_file.name)
    target = EVIDENCE / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_{safe}"
    target.write_bytes(uploaded_file.getvalue())
    return str(target.relative_to(BASE))


def add_evidence_placeholders(uploaded_files):
    data = load_credentials()
    added = []
    for uf in uploaded_files or []:
        path = save_evidence(uf)
        item = {
            "id": uuid.uuid4().hex,
            "name": Path(uf.name).stem.replace("_", " ").strip(),
            "issuer": "",
            "type": "Certification",
            "date": "",
            "credential_id": "",
            "verification_url": "",
            "skills": [],
            "status": "Needs review",
            "evidence_files": [path],
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "completed_at": "",
            "notes": "",
        }
        data["items"].append(item)
        added.append(item)
    save_credentials(data)
    return added


def update_credential(item_id, updates):
    data = load_credentials()
    for item in data["items"]:
        if item.get("id") == item_id:
            item.update(updates)
            if updates.get("status") == "Completed" and not item.get("completed_at"):
                item["completed_at"] = datetime.now().isoformat(timespec="seconds")
            save_credentials(data)
            return item
    return None


def delete_credential(item_id):
    data = load_credentials()
    keep = []
    for item in data["items"]:
        if item.get("id") == item_id:
            for rel in item.get("evidence_files", []):
                p = BASE / rel
                if p.exists():
                    try:
                        p.unlink()
                    except Exception:
                        pass
        else:
            keep.append(item)
    data["items"] = keep
    save_credentials(data)


def completions_this_week():
    now = datetime.now()
    start = (now - timedelta(days=now.weekday())).date()
    count = 0
    for item in load_credentials().get("items", []):
        raw = item.get("completed_at") or ""
        if not raw:
            continue
        try:
            dt = datetime.fromisoformat(raw).date()
            if dt >= start:
                count += 1
        except Exception:
            pass
    return count


def credential_streak(goal):
    goal = int(goal)
    items = load_credentials().get("items", [])
    dates = []
    for item in items:
        raw = item.get("completed_at") or ""
        try:
            dates.append(datetime.fromisoformat(raw).date())
        except Exception:
            pass
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    streak = 0
    for w in range(52):
        start = monday - timedelta(days=w * 7)
        end = start + timedelta(days=6)
        count = sum(1 for d in dates if start <= d <= end)
        if w == 0 and count < goal:
            continue
        if count >= goal:
            streak += 1
        else:
            break
    return streak


def sync_verified_profile():
    """Push completed confirmed credentials/honors into the verified candidate profile."""
    from profile_store import load_candidate_profile, save_candidate_profile
    profile = load_candidate_profile()
    certs, awards = [], []
    for item in load_credentials().get("items", []):
        if item.get("status") != "Completed" or not item.get("name"):
            continue
        out = {
            "name": item.get("name", ""),
            "date": item.get("date", ""),
            "issuer": item.get("issuer", ""),
            "credential_id": item.get("credential_id", ""),
            "verification_url": item.get("verification_url", ""),
        }
        if item.get("type") in {"Honor", "Award", "Academic Honor"}:
            awards.append(out)
        else:
            certs.append(out)
    profile["certifications"] = certs
    profile["awards"] = awards
    save_candidate_profile(profile)
    return len(certs), len(awards)
