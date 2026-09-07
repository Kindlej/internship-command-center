# V13 — Career Operating System

V13 is the first release that treats Internship Command Center as a cohesive career workflow rather than a collection of tools.

## Product changes

- Replaces crowded top-level tabs with persistent sidebar navigation and a new dashboard hierarchy.
- Adds adjustable daily application goals from 2–6 applications/day, with progress and completed-goal streak tracking.
- Adds adjustable weekly credential goals from 2–6 credentials/week.
- Adds a Career Calendar that can render Scout posting timestamps, confirmed submissions, and follow-up events, with room for richer source/deadline/interview events later.
- Adds Credentials & Honors with multi-file image/PDF evidence intake, local evidence storage, confirmation fields, status tracking, and verified-profile synchronization.
- Seeds a credential learning library covering data science, analytics, AI, cloud, SQL, and data engineering providers. Cost labels deliberately distinguish free training from a free official credential when terms are uncertain.
- Adds Resume Studio with three content strategies and six single-column visual themes.
- Adds ATS Lab with transparent scoring for keyword coverage, verified skill coverage, structure, action language, evidence strength, and parsing safety.
- Adds explicit user confirmation for final application submission so progress goals count real submitted applications rather than automated browser launches.
- Keeps recruiter research manual instead of silently running it during application launch.

## Resume strategies

Content strategy and visual styling are independent. Supported content strategies are Reverse-Chronological, Combination / Hybrid, and Functional / Skills-Based. Supported visual themes are Jake / Technical, Modern / Contemporary, Traditional / Conservative, Minimal, Campus / Recent Graduate, and Conservative Finance.

All themes remain single-column by default. Functional / Skills-Based mode carries a visible ATS-risk warning because some recruiters and parsers prefer chronological history.

## ATS Lab philosophy

V13 does not claim to emulate a proprietary employer ATS. Its score is an explainable readiness heuristic that surfaces which job-language terms are supported, which skills appear in the job description, which are present in the resume, whether standard sections exist, and where formatting or evidence could be improved. Missing skills are never auto-added unless they are verified candidate facts.

## Privacy

The public repository excludes real candidate profiles, application answers, databases, generated documents, browser profiles, API keys, credential evidence, credential records, goal settings, and resume preferences.

## Test status

The local V13 build passes the new feature test suite covering goal ranges, resume-format configuration, seeded credential providers, and ATS score bounds/truthfulness. Full Streamlit visual smoke testing still requires running the app in an environment with Streamlit installed.
