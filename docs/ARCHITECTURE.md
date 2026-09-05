# Internship Command Center v12 Architecture

## Core flow

1. **Scout** reads configured public ATS boards (Greenhouse, Lever, Ashby), validates source health, normalizes postings, deduplicates across sources, and applies cheap local eligibility/keyword scoring before AI spend.
2. **Evaluator** compares a posting with the current verified candidate profile and produces a fit score, recommendation, top strengths, top gaps, and hard-eligibility warning.
3. **Pipeline** stores the opportunity lifecycle: DISCOVERED → EVALUATED → SUGGESTED / QUALIFIED → PACKAGING → READY → APPLYING → SUBMITTED → FOLLOW_UP, plus ARCHIVED.
4. **Document builder** asks the configured provider to prioritize/rewrite only verified facts, then renders the final résumé deterministically in an ATS-safe single-column DOCX/PDF layout. Cover letters are role-specific and versioned alongside the résumé manifest.
5. **Application assistant** uses reusable known answers and generated files to help populate forms. Sensitive/unknown answers remain manual and final submission is outside the agent's authority.
6. **Connections** open account-based marketplaces in persistent local browser profiles or the normal system browser without storing passwords or bypassing provider security.

## Main modules

- `app.py` — Streamlit orchestration, SQLite schema/migrations, pipeline actions, dashboard views.
- `ui.py` — command-center design tokens and CSS.
- `scout.py` — public ATS connectors, normalization, deduplication, local pre-scoring.
- `job_ingest.py` — URL ingestion and Parsed / Partial / Failed classification.
- `llm_provider.py` — Gemini/OpenAI/Anthropic provider abstraction and usage/budget accounting.
- `resume_renderer.py` — deterministic ATS-safe résumé and cover-letter document rendering/versioning.
- `profile_store.py` — current candidate-profile persistence and backups.
- `application_assistant.py` — Playwright-based human-in-the-loop form assistance.
- `browser_connections.py` — local account-connection/browser helpers.
- `people_research.py` — public professional recruiter/hiring-team research boundary.

## Data boundary

Personal data remains local: candidate profile, reusable application answers, SQLite history, generated documents, attachments, browser sessions, and provider secrets. Public GitHub exports use example schemas instead of real candidate data.

## Automation boundary

The system may automate discovery, scoring, packaging, safe known-field filling, and non-final navigation. It does not bypass authentication/security controls and does not perform the final application submission.
