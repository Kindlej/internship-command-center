# V14 Tailoring Architecture

V14 makes resume tailoring the primary quality system rather than a one-shot rewrite.

## Pipeline
1. Parse the target job and its fit evaluation.
2. Rank verified evidence from experience, projects, coursework, credentials, honors, and leadership.
3. Allocate scarce one-page space to the strongest evidence instead of preserving every source equally.
4. Generate source-cited bullets: each rewritten bullet maps to one verified source fact.
5. Run a deterministic quality review for job alignment, evidence strength, bullet quality, information density, redundancy, and truth integrity.
6. In Deep mode, run a second LLM refinement pass when the first draft falls below the configured quality gate.
7. Render the selected ATS-safe visual theme.
8. Run ATS readiness against the actual rendered resume text.
9. Persist the spec, quality review, ATS review, profile snapshot, and versioned document.

## V14 benchmark template
`High-Density Professional` is a conservative single-column serif layout inspired by strong consulting/finance resumes: compact spacing, thin section rules, right-aligned dates/locations, and high page utilization. It does not use tables, text boxes, sidebars, graphics, or multi-column content.

## Truth boundary
A model may prioritize, omit, reorder, and rewrite verified evidence. It may not create a metric, tool, credential, employer, project, date, responsibility, or outcome that is absent from the verified profile. Missing evidence is surfaced as a gap rather than fabricated.
