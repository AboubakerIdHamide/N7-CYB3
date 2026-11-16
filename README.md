# CYB-3 — Autonomous Agent Reliability on Security Challenges

This is a scientific evaluation project, not a production penetration-testing product. It will study repeated success, tool-harness sensitivity, and cost per solved CTF challenge, following the course brief.

## Current status

- Research question: a working rephrasing of the teacher's CYB-3 question is in `RESEARCH_PLAN_DRAFT.md`.
- Candidate model: `qwen3:1.7b` through local Ollama. This is a feasibility choice, not yet the final experimental model.
- A local Buffer Overflow 0 teaching target is now scaffolded under `challenges/buffer_overflow_0/`. It is a candidate for the first pilot, not yet a final benchmark selection.
- A first restricted agent tool wrapper is in place; the benchmark protocol and second harness are still to be designed before the main experiment.
- The first agent pilot ran but did not solve the challenge; its summary and evidence are in `results/pilots/2026-11-15-attempt-001.md`.
- A second pilot hit the six-action limit after repeating short inputs; its trace and logging issues are recorded in `results/pilots/2026-11-16-attempt-002.md`.
- The code now includes a harmless local tool-call pilot. It does not contact a target or run security actions.

## Safety and scope

When the experiment is eventually run, use only public CTF challenges or intentionally vulnerable machines in an isolated environment, with no real targets. Follow the teacher's written-authorization requirement. Do not use this repository to test systems outside the approved lab.

## Experiment requirements to preserve

- Repeated attempts on each challenge and two tool harnesses.
- Complete run logs and a failure taxonomy.
- `pass@1`, `pass^k`, steps, cost per solved challenge, and the share of failures attributable to the harness.
- At least three seeds, a baseline, an ablation, error analysis, and reproducible configuration.

## Current code components

`src/cyb3/runlog.py` defines a run record and appends records to JSON Lines. It is deliberately independent of the model provider and lab.

`scripts/local_tool_pilot.py` sends a calculator-only tool call to the local Ollama service, runs that allowlisted addition, and returns the result to the model. On 2026-11-15, `qwen3:1.7b` requested `add_numbers(23, 19)`, the script returned `42`, and the model replied with the correct sum. This confirms the local model-tool-model loop works; it is not evidence of CTF-solving ability.

`challenges/buffer_overflow_0/` contains a deliberately vulnerable, local-only C challenge and a fake flag template. Its Docker image was built and checked with networking disabled and container resource limits. The first restricted agent wrapper is now in place; do not expose an unrestricted shell to the model.

`scripts/local_ctf_agent.py` is the first restricted agent prototype. It gives the local Ollama model only two fixed tools: read this one C source file, and send up to 120 printable ASCII characters to the fixed Docker image. It allows at most six tool actions per attempt. The Docker command is hard-coded, uses no shell or host mounts, never pulls images, disables container networking, and applies non-root, read-only, capability, process, memory, CPU, and timeout limits. The script records a JSONL run summary and a trace of tool calls plus the model's final answer under ignored `outputs/`.

To start one pilot attempt, ensure Ollama is running and the Docker image has been built, then run from the project root:

```sh
python3 scripts/local_ctf_agent.py
```

This is a feasibility prototype, not yet the final benchmark harness: it has one fixed seed, one attempt, and one tool configuration. If run through Codex, Docker access may require approval because the restricted command sandbox blocks Docker's socket; running it in your own terminal uses your host's Docker permissions. Do not use it for other targets or give the model an unrestricted shell.

## Decisions still open

Choose the agent/model, safe challenge suite, the two harnesses, the value of `k`, run limits, and the final failure categories before running the main experiment. Avoid paid API calls until the model route and budget are clear.
