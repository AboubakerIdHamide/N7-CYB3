# CYB-3 — Autonomous Agent Reliability on Security Challenges

This is a scientific evaluation project, not a production penetration-testing product. It will study repeated success, tool-harness sensitivity, and cost per solved CTF challenge, following the course brief.

## Current status

- Research question: a working rephrasing of the teacher's CYB-3 question is in `RESEARCH_PLAN_DRAFT.md`.
- No agent, model, challenge set, or harness has been selected yet.
- The first code component records run outcomes. It does not connect to a model, execute tools, or contact a target.

## Safety and scope

When the experiment is eventually run, use only public CTF challenges or intentionally vulnerable machines in an isolated environment, with no real targets. Follow the teacher's written-authorization requirement. Do not use this repository to test systems outside the approved lab.

## Experiment requirements to preserve

- Repeated attempts on each challenge and two tool harnesses.
- Complete run logs and a failure taxonomy.
- `pass@1`, `pass^k`, steps, cost per solved challenge, and the share of failures attributable to the harness.
- At least three seeds, a baseline, an ablation, error analysis, and reproducible configuration.

## First code component

`src/cyb3/runlog.py` defines a run record and appends records to JSON Lines. It is deliberately independent of the model provider and lab. Later, an experiment runner can call this logger after a run.

## Decisions still open

Choose the agent/model, safe challenge suite, the two harnesses, the value of `k`, run limits, and the final failure categories before running the main experiment. Avoid paid API calls until the model route and budget are clear.
