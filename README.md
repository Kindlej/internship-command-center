# Internship Command Center

A local-first, human-in-the-loop AI system for discovering internships, evaluating fit against verified candidate facts, generating ATS-safe application materials, and organizing the entire application pipeline without surrendering final-submit control.

> Current release: **v12.0.0**

## Why this exists

Internship searching is repetitive: checking career boards, reading nearly identical descriptions, deciding whether a role is worth applying to, tailoring a resume, writing a cover letter, tracking status, and remembering follow-ups. Internship Command Center turns those steps into one controlled workflow while keeping candidate facts and sensitive application decisions under human control.

## What v12 does

- Scouts configured public Greenhouse, Lever, and Ashby company boards.
- Validates ATS source URLs before saving them.
- Deduplicates and cheaply filters postings before spending AI tokens.
- Batch-evaluates 5, 10, 25, or 50 discovered roles against a verified profile.
- Explains fit with strengths, gaps, and hard-eligibility warnings.
- Uses a pipeline: `DISCOVERED → EVALUATED → SUGGESTED → QUALIFIED → PACKAGING → READY → APPLYING → SUBMITTED → FOLLOW_UP`, with `ARCHIVED` for weak or ineligible matches.
- Can auto-build 85+ fit opportunities subject to a daily cap.
- Generates role-specific one-page ATS-safe resumes and cover letters.
- Versions generated application materials and stores a change manifest.
- Keeps reusable application answers separate from generated prose.
- Provides normal-browser connection helpers for LinkedIn, Handshake, Indeed, ZipRecruiter, Glassdoor, Wellfound, Built In, and Dice.
- Assists with safe form filling but deliberately stops before final submission.
- Supports Gemini, OpenAI, and Anthropic provider routing with budget controls.
- Restricts recruiter research to public professional information.

## Product principles

**Verified facts only.** Resume and application generation may prioritize or rewrite verified information, but it may not invent experience, skills, dates, credentials, education, or accomplishments.

**Human final authority.** The system can discover, evaluate, package, and assist. It does not click the final submit/apply/send/complete action.

**No security bypasses.** It does not defeat CAPTCHAs, login walls, provider bot protections, or Google security controls. Normal browser login is preferred for account-based job marketplaces.

**Local-first privacy.** Personal candidate data, application answers, databases, browser profiles, API keys, attachments, and generated applications are excluded from the public repository.

## Architecture

```text
Public ATS boards / job URLs
          │
          ▼
       Scout
          │
   dedupe + cheap filter
          │
          ▼
      Evaluator
          │
  fit score + explanation
          │
          ▼
 Application Pipeline
          │
   ┌──────┼─────────┐
   ▼      ▼         ▼
Resume  Cover     Answers
Tailor  Letter    Builder
   └──────┼─────────┘
          ▼
       READY
          │
          ▼
 Browser Assistant
          │
          ▼
 Human review + submit
```

See `docs/ARCHITECTURE.md` for the component breakdown.

## Quick start

Requires Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m streamlit run app.py
```

On Windows, activate the virtual environment with the Windows equivalent or use the included installer/start scripts.

Configure at least one provider key in your environment. Never commit API keys.

```bash
export GEMINI_API_KEY="..."
# or OPENAI_API_KEY / ANTHROPIC_API_KEY
```

## Public vs. local files

The repository is intentionally safe to make public. These stay local and are ignored by Git:

```text
candidate_profile.json
application_answers.json
applications.db
.env
.browser_profile/
.connected_browser_profiles/
connection_state.json
profile_attachments/
profile_history/
generated/
.venv/
```

Use `candidate_profile.example.json` and `application_answers.example.json` as schemas/examples rather than committing real personal data.

## Development

Run core tests:

```bash
python -m unittest discover -s tests -v
```

Compile-check the project:

```bash
python -m compileall -q .
```

GitHub Actions runs these checks on pushes and pull requests.

## Current v12 focus

V12 is the command-center/UI and workflow-polish release: roomier wrapped navigation, stronger dark/light visual tokens, source health validation, batch evaluation, high-fit auto-build controls, safer normal-browser account connections, CI-ready tests, and a cleaner public project structure.

## Roadmap

The next high-value areas are persistent generated-document paths, richer outcome analytics, cost-per-application/interview reporting, company application-frequency guards, scheduled digest/follow-up workflows, stronger semantic deduplication, interview-prep workflows, and deeper end-to-end tests.

## Safety boundary

This project is an application assistant, not an autonomous final-submission bot. Unknown or sensitive legal/personal questions remain manual. Recruiter research is limited to public professional context. Website automation is best-effort and must respect provider restrictions.

## Author

Built by Jeremy Kindle as a practical data/AI automation project for managing the internship search and application process.
