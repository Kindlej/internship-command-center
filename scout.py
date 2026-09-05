"""Public ATS discovery core for Internship Command Center.

This module intentionally supports public Greenhouse, Lever, and Ashby job-board
endpoints only. Account-based marketplaces are handled through normal browser
connections rather than scraping or authentication bypasses.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse

import requests

from profile_store import load_candidate_profile

BASE = Path(__file__).parent
SOURCES_PATH = BASE / "sources.json"


@dataclass
class Job:
    source: str
    company: str
    external_id: str
    title: str
    location: str
    url: str
    description: str

    def to_dict(self):
        return asdict(self)


def parse_source_url(url: str):
    """Return (provider, board token) for a supported public ATS URL."""
    parsed = urlparse((url or "").strip())
    host = parsed.netloc.lower().removeprefix("www.")
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        raise ValueError("The source URL does not contain a company board token.")
    token = parts[0]
    if host in {"boards.greenhouse.io", "job-boards.greenhouse.io"}:
        return "greenhouse", token
    if host == "jobs.lever.co":
        return "lever", token
    if host == "jobs.ashbyhq.com":
        return "ashby", token
    raise ValueError("Supported public sources are Greenhouse, Lever, and Ashby company boards.")


def _clean_html(value: str):
    value = re.sub(r"<br\s*/?>", "\n", value or "", flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _get_json(url, **kwargs):
    response = requests.get(url, timeout=20, headers={"User-Agent": "InternshipCommandCenter/12"}, **kwargs)
    response.raise_for_status()
    return response.json()


def validate_source(url: str):
    provider, token = parse_source_url(url)
    if provider == "greenhouse":
        data = _get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
        count = len(data.get("jobs", []))
    elif provider == "lever":
        data = _get_json(f"https://api.lever.co/v0/postings/{token}", params={"mode": "json"})
        count = len(data if isinstance(data, list) else [])
    else:
        data = _get_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
        count = len(data.get("jobs", []))
    return {"ok": True, "provider": provider, "token": token, "openings": count}


def fetch_source(url: str):
    provider, token = parse_source_url(url)
    if provider == "greenhouse":
        data = _get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs", params={"content": "true"})
        return [Job("greenhouse", token, str(j.get("id", "")), j.get("title", ""), (j.get("location") or {}).get("name", ""), j.get("absolute_url", ""), _clean_html(j.get("content", ""))) for j in data.get("jobs", [])]
    if provider == "lever":
        data = _get_json(f"https://api.lever.co/v0/postings/{token}", params={"mode": "json"})
        return [Job("lever", token, str(j.get("id", "")), j.get("text", ""), ((j.get("categories") or {}).get("location") or ""), j.get("hostedUrl", ""), _clean_html(j.get("descriptionPlain") or j.get("description", ""))) for j in data]
    data = _get_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
    return [Job("ashby", token, str(j.get("id", j.get("jobUrl", ""))), j.get("title", ""), j.get("location", ""), j.get("jobUrl", ""), _clean_html(j.get("descriptionPlain") or j.get("descriptionHtml", ""))) for j in data.get("jobs", [])]


def normalize_title(title: str):
    text = re.sub(r"[^a-z0-9]+", " ", (title or "").lower())
    return " ".join(text.split())


def dedupe_jobs(jobs):
    seen, output = set(), []
    for job in jobs:
        key = (job.company.lower().strip(), normalize_title(job.title), job.url.lower().strip())
        if key in seen:
            continue
        seen.add(key)
        output.append(job)
    return output


def keyword_score(job: Job):
    profile = load_candidate_profile()
    text = f"{job.title} {job.description}".lower()
    title = job.title.lower()
    score = 45
    reasons = []

    internship_terms = ("intern", "internship", "student", "co-op", "coop")
    if any(term in title for term in internship_terms):
        score += 25
        reasons.append("intern/student role")

    target_terms = ("data", "analytics", "business intelligence", "bi ", "sql", "engineering")
    if any(term in title for term in target_terms):
        score += 12
        reasons.append("target role family")

    skills = [str(s) for s in profile.get("verified_skills", []) if str(s).strip()]
    matches = [skill for skill in skills if skill.lower() in text]
    score += min(20, len(matches) * 4)
    if matches:
        reasons.append("skills: " + ", ".join(matches[:5]))

    senior_terms = ("senior", "staff", "principal", "manager", "director", "lead ")
    if any(term in title for term in senior_terms):
        score -= 45
        reasons.append("senior-level title penalty")

    experience_match = re.search(r"(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience", text)
    if experience_match and int(experience_match.group(1)) >= 3:
        score -= 25
        reasons.append("3+ years experience requirement")

    return max(0, min(100, score)), reasons


def load_sources():
    if not SOURCES_PATH.exists():
        return []
    data = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("sources", [])


def scout_all(sources=None):
    sources = sources if sources is not None else load_sources()
    jobs, errors = [], []
    for source in sources:
        url = source if isinstance(source, str) else source.get("url", "")
        if not url:
            continue
        try:
            jobs.extend(fetch_source(url))
        except Exception as exc:
            errors.append({"url": url, "error": str(exc)})
    jobs = dedupe_jobs(jobs)
    ranked = []
    for job in jobs:
        score, reasons = keyword_score(job)
        ranked.append({**job.to_dict(), "pre_score": score, "pre_score_reasons": reasons})
    ranked.sort(key=lambda item: item["pre_score"], reverse=True)
    return {"jobs": ranked, "errors": errors}


if __name__ == "__main__":
    print(json.dumps(scout_all(), indent=2))
