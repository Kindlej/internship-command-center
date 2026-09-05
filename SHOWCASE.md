# Internship Command Center — Showcase Notes

## One-line pitch
A local-first AI internship workflow that discovers roles, evaluates fit against verified profile facts, generates ATS-safe tailored materials, and keeps the student in control of final submission.

## What the project demonstrates
- Public ATS integration for Greenhouse, Lever, and Ashby
- Source validation, keyword eligibility filtering, and cross-source deduplication before AI spend
- Batch LLM evaluation with explainable fit states
- Editable single-source-of-truth candidate profile
- One-page ATS-safe résumé rendering and versioned application materials
- URL ingestion with explicit Parsed / Partial / Failed states
- Human-in-the-loop browser application assistance
- Recruiter research restricted to public professional information
- Provider routing and budget controls for Gemini, OpenAI, and Anthropic
- Local browser connection helpers for job marketplaces without bypassing provider security
- SQLite-backed application state/history and outcome tracking
- Dark/light command-center UI designed around an application pipeline

## Product/safety boundary
The system does not invent candidate facts, defeat login/CAPTCHA protections, collect account passwords, or click the final application submit button.

## Engineering angle
This project combines data ingestion, normalization, state-machine design, local persistence, LLM orchestration, document generation, browser automation, privacy boundaries, testing, and product/UI design in one practical workflow.
