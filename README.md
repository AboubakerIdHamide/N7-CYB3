# CYB-3 — Autonomous Agent Reliability on Security Challenges

This is a scientific evaluation project, not a production penetration-testing product. It will study repeated success, tool-harness sensitivity, and cost per solved CTF challenge, following the course brief.

## Current status

- Research question: a working rephrasing of the teacher's CYB-3 question is in `RESEARCH_PLAN_DRAFT.md`.
- Candidate model: `qwen3:1.7b` through local Ollama. This is a feasibility choice, not yet the final experimental model.
- Three local, intentionally vulnerable CTF-style targets are scaffolded: Buffer Overflow 0, integer wrap, and path traversal. Their suite selection remains provisional until the protocol is frozen.
- The restricted agent runner now supports raw output, structured feedback, and a structured-feedback ablation without the flag indicator. The evaluator scores the real output, then removes the exact dummy flag before showing output to the agent, so the explicit indicator is a genuine feedback difference. The comparison design is in `EXPERIMENT_PROTOCOL_DRAFT.md`; it is not frozen and no main experiment has run.
- `scripts/build_challenges.sh` builds the three local images. `scripts/run_experiment.py` defines the reproducible 27-run matrix and refuses to run while the protocol remains a draft.
- The first agent pilot ran but did not solve the challenge; its summary and evidence are in `results/pilots/2026-11-15-attempt-001.md`.
- A second pilot hit the six-action limit after repeating short inputs; its trace and logging issues are recorded in `results/pilots/2026-11-16-attempt-002.md`.
- On 2026-11-21, two launch attempts could not reach Ollama and stopped before any challenge action. They are recorded as infrastructure failures, not agent-solving results, in `results/pilots/2026-11-21-preflight-launch-failure.md`.
- A later valid attempt 003 reached the six-action limit after repeating short inputs; its trace and final model summary are recorded in `results/pilots/2026-11-21-attempt-003.md`.
- Attempt 004 used prompt `source_guided_v2`, but the agent stopped after two harmless inputs without completing the attempt it described. Its trace is recorded in `results/pilots/2026-11-21-attempt-004.md`.
- Calibration on 2026-11-21 confirmed the local integer-wrap and path-traversal targets work with known inputs, but Qwen 3 1.7B failed every agent run. Prompt v4 fixed malformed source-tool calls in one task, but the model still failed to reason through the challenge. These are calibration failures, not baseline-comparison results; see `results/pilots/2026-11-21-integer-wrap-calibration.md`, `results/pilots/2026-11-21-path-traversal-calibration.md`, and `results/pilots/2026-11-21-path-traversal-calibration-v4.md`.
- A matched three-seed calibration on path traversal (`source_guided_v4`) produced 0/3 solves with both raw and structured feedback. This is a floor effect, not evidence that the harnesses are equivalent; do not launch the full matrix until model/task feasibility is resolved. See `results/pilots/2026-11-21-path-v4-k3.md`.
- A Qwen3 1.7B thinking-mode pair also produced no solves and took 3–4 minutes per run. Qwen3 4B loaded on CPU, but two raw-feedback pilots ended before a challenge input; the 768-token retry took over four minutes. These model-feasibility failures and their run traces are in `results/pilots/2026-11-21-path-thinking-pilot.md` and `results/pilots/2026-11-22-path-qwen3-4b-pilot.md`.
- Prompt/tool-use calibration on 2026-11-22 made the 1.7B agent submit actions, but it still repeated nonexistent paths after tool errors; v5/v6 both failed. Stop repeating local 1.7B trials. Next, check whether Qwen3 4B can run quickly on a Colab GPU, then verify that the Docker challenge remains isolated before moving the full experiment. See `results/pilots/2026-11-22-path-prompt-calibration.md`.
- The runner now assigns attempt numbers from comparable prior runs, accepts a configurable generation seed, records a final summary after the action limit, and starts a trace before contacting Ollama.
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

`challenges/` contains three deliberately vulnerable, local-only C challenges and fake flag templates. Build their fixed images from the project root with:

```sh
sh scripts/build_challenges.sh
```

The runner keeps networking disabled and applies container resource limits; do not expose an unrestricted shell to the model.

`scripts/local_ctf_agent.py` gives the local Ollama model only two fixed tools: read the selected allowlisted C source and send up to 120 printable ASCII characters to its fixed image. Select a task with `--challenge-id` and one of three feedback conditions with `--harness`: `raw_output_v1`, `structured_feedback_v1`, or `structured_no_flag_v1`. The Docker command is hard-coded, uses no shell or host mounts, never pulls images at run time, disables container networking, and applies non-root, read-only, capability, process, memory, CPU, and timeout limits. Each attempt has at most six tool actions. The script records a JSONL run summary and a full action trace under `outputs/`.

To start one pilot attempt, ensure Ollama is running and the fixed Docker images have been built, then run from the project root:

```sh
python3 scripts/local_ctf_agent.py --challenge-id local_buffer_overflow_0 --harness structured_feedback_v1 --seed 42
```

The main matrix launcher is `python3 scripts/run_experiment.py`; it runs only after the protocol status is changed to frozen. It preflights Ollama and checks that the fixed local images exist, records model and image identifiers plus exact prompt text, randomizes the run order reproducibly, and stops if an infrastructure failure occurs. Attempt numbers are assigned from prior completed runs for the same challenge, harness, model, and seed; infrastructure failures marked `incomplete` do not consume an attempt number. Use `--attempt N` only when intentionally setting one. Start Ollama before running. If run through Codex, Docker access may require approval because the restricted command sandbox blocks Docker's socket; running it in your own terminal uses your host's Docker permissions. Do not use it for other targets or give the model an unrestricted shell.

## Decisions still open

Freeze the exact challenge versions, prompt, run order, seeds, and failure categories before running the main experiment. Avoid paid API calls; the current protocol uses a local model.
