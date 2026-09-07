import re
from collections import Counter

STOP = {
    "and","or","the","a","an","to","of","in","for","with","on","at","by","from","as","is","are","be","this","that",
    "you","your","we","our","will","can","may","job","role","work","team","intern","internship","candidate","preferred","required",
}

SKILL_TERMS = [
    "python","sql","pandas","numpy","tableau","power bi","excel","snowflake","azure","aws","gcp","bigquery","etl","data pipeline",
    "machine learning","statistics","analytics","data visualization","business intelligence","spark","databricks","postgresql","mysql","git",
    "scikit-learn","tensorflow","pytorch","r","java","c++","airflow","dbt","looker","powerpoint","communication","stakeholder",
]

ACTION_VERBS = {
    "analyzed","built","created","developed","designed","implemented","improved","automated","cleaned","modeled","visualized","presented",
    "managed","led","optimized","validated","transformed","queried","integrated","evaluated","delivered","supported","collaborated","monitored",
}


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _keywords(text, n=35):
    t = _norm(text)
    tokens = re.findall(r"[a-z][a-z0-9+.#-]{2,}", t)
    counts = Counter(x for x in tokens if x not in STOP)
    return [w for w, _ in counts.most_common(n)]


def scan_resume(resume_text, job_description, *, structural_format="Reverse-Chronological"):
    resume = _norm(resume_text)
    jd = _norm(job_description)
    jd_keywords = _keywords(jd, 40)
    matched = [k for k in jd_keywords if re.search(rf"\b{re.escape(k)}\b", resume)]
    keyword_score = round(100 * len(matched) / max(1, len(jd_keywords)))

    required_skills = [s for s in SKILL_TERMS if s in jd]
    matched_skills = [s for s in required_skills if s in resume]
    skill_score = round(100 * len(matched_skills) / max(1, len(required_skills))) if required_skills else 80

    standard_sections = ["education", "experience", "skills"]
    section_hits = sum(1 for s in standard_sections if s in resume)
    structure_score = round(100 * section_hits / len(standard_sections))
    if structural_format == "Functional / Skills-Based":
        structure_score = max(55, structure_score - 12)

    lines = [x.strip() for x in (resume_text or "").splitlines() if x.strip()]
    bulletish = [x for x in lines if x.startswith(("•", "-", "*")) or len(x.split()) >= 7]
    action_hits = sum(1 for x in bulletish if x.split()[0].lower().strip("•-*.,:") in ACTION_VERBS)
    action_score = round(100 * action_hits / max(1, min(len(bulletish), 12))) if bulletish else 45

    metric_hits = len(re.findall(r"\b\d+(?:\.\d+)?%|\b\d+[+,]?\b", resume_text or ""))
    evidence_score = min(100, 55 + metric_hits * 8)

    formatting_score = 96
    risky = []
    if "|" in (resume_text or "") and (resume_text or "").count("|") > 12:
        formatting_score -= 10
        risky.append("Dense pipe-separated content can parse inconsistently.")
    if structural_format == "Functional / Skills-Based":
        risky.append("Pure skills-based resumes can be harder for some ATS/recruiters to interpret than chronological or hybrid formats.")

    overall = round(keyword_score * .30 + skill_score * .25 + structure_score * .15 + action_score * .10 + evidence_score * .10 + formatting_score * .10)
    overall = max(0, min(100, overall))

    missing_keywords = [k for k in jd_keywords if k not in matched][:10]
    missing_skills = [s for s in required_skills if s not in matched_skills][:8]
    improvements = []
    if missing_skills:
        improvements.append("Verify whether your profile supports these job skills before adding them: " + ", ".join(missing_skills[:5]))
    if keyword_score < 75:
        improvements.append("Increase truthful job-language coverage by rewriting verified bullets with supported terminology.")
    if action_score < 70:
        improvements.append("Start more bullets with clear action verbs and keep each bullet outcome-focused.")
    if metric_hits < 2:
        improvements.append("Where verified metrics exist, surface them; never invent numbers just to raise this score.")
    if structure_score < 80:
        improvements.append("Use standard headings such as Education, Skills, Experience, and Projects.")

    return {
        "overall": overall,
        "keyword_coverage": keyword_score,
        "skill_coverage": skill_score,
        "structure": structure_score,
        "action_language": action_score,
        "evidence_strength": evidence_score,
        "formatting_safety": formatting_score,
        "matched_keywords": matched[:15],
        "missing_keywords": missing_keywords,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "risks": risky,
        "improvements": improvements[:6],
        "disclaimer": "ATS Readiness is a transparent heuristic, not a prediction of any employer's proprietary ATS ranking."
    }
