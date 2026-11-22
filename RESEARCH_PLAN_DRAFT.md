# CYB-3 research plan — draft

**Status (2026-11-22):** feasibility calibration. The local `qwen3:1.7b` agent loop works, and the local targets pass known-input checks. It failed all ten valid agent calibration runs across integer-wrap and path-traversal tasks. On the path task, prompt v4 fixed malformed source-tool calls, but the matched raw and structured conditions each scored 0/3 across three seeds and exhausted the action limit. Enabling thinking mode did not produce a solve and raised each run to 3–4 minutes. Qwen3 4B loaded on CPU, but two raw-feedback pilots ended without solving; the longer run took 4 minutes 18 seconds and stopped after reading the source. This is a floor effect, not evidence that the harnesses are equivalent. The protocol remains a draft; no main experiment has run. See `results/pilots/` for evidence.

## 1. Teacher's topic and research question

**Topic:** Reliability of autonomous agents on security challenges.

The catalogue asks how reliable a penetration-testing agent is on CTF challenges when we consider repeated success, sensitivity to the tool harness, and cost per solved challenge.

**Working rephrasing:**

> How reliably does an autonomous penetration-testing agent solve CTF challenges across repeated attempts, how does its tool harness affect that reliability, and what is the cost per challenge solved?

This rephrases the teacher's question; it does not change the topic.

## 2. Requirements from the teacher's documents

- Use public CTF challenges or intentionally vulnerable machines in an isolated environment; do not test real targets.
- Make repeated attempts on each challenge and compare two tool harnesses.
- Keep complete run logs and classify failures.
- Report `pass@1`, `pass^k`, number of steps, cost per solved challenge, and the share of failures attributed to the harness.
- State the protocol before the main experiment, include at least three seeds, and report mean and standard deviation.
- Include a baseline, an ablation, error analysis, and enough environment/configuration details for a reproducible rerun.
- Prepare 15–25 references (a majority from the last three years), an 8–12 page article, a 12–15 slide editable presentation, and code with an environment file and a single-command README.

## 3. Experiment shape to investigate

The proposed fair comparison holds the agent/model, challenge, tools, prompt, and run limits constant while changing the output format of tool results. The evaluator scores the original challenge output, then redacts the exact dummy flag from all model-visible output. The candidate baseline returns raw standard output and error; the structured condition returns a JSON object with execution metadata and an explicit success indicator; the ablation removes that indicator. The definitions are in `EXPERIMENT_PROTOCOL_DRAFT.md` and remain subject to review before the main runs.

Candidate outcomes:

- Success rate on the first attempt (`pass@1`).
- Success across `k` repeated attempts (`pass^k`; choose and justify `k` in the protocol).
- Cost per successful challenge, number of steps, and elapsed time.
- Failure categories and the share attributable to the harness.

## 4. Decisions still needed before the main experiment

1. The 1.7B model did not solve either calibrated task; the matched path study scored 0/3 in both conditions. Choose a capable model or a task/configuration that produces informative outcomes before freezing.
2. Decide whether the three candidate tasks form a manageable, honestly scoped suite; do not assume all are needed.
3. Recheck that only tool-result feedback differs across the baseline, structured condition, and ablation.
4. Freeze the seeds, action cap, reset procedure, and flag-based success criterion after calibration.

## 5. Work after calibration

The matrix runner and run-log schema are implemented. Next, choose a model/task setup that can demonstrate at least some successful solves, then rerun a small matched calibration. Freeze the protocol only after this feasibility check; do not spend time or compute on the 27-run matrix while all calibration outcomes are failures.

## 6. Schedule note

As of 2026-11-21, the November 3 first-results checkpoint has passed and the November 24 checkpoint for complete results, ablations, and error analysis is three days away. Final submission is December 8. The current work is behind the intended research schedule; prioritize a narrow but honest reproducible study, and report any unmet intermediate checkpoint accurately. Do not present exploratory pilots as complete results.

## 7. Immediate recovery sequence

1. Resolve the calibration floor effect: the current 1.7B model failed all ten valid attempts on integer-wrap and path-traversal, including a matched three-seed path comparison.
2. Confirm the chosen model and task can yield informative outcomes, then freeze the protocol, metrics, and run order before collecting main results.
3. Run the smallest complete comparison that can be finished and rerun before December 8. Record any reduction in scope as a limitation, not as a result that the study did not measure.
