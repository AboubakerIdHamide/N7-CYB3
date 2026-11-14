# CYB-3 research plan — draft

**Status:** planning only. No agent, challenge set, or experiment has been selected or run yet.

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

The simplest fair comparison is likely to hold the agent/model, challenges, tools, prompts, and run limits constant while changing the tool harness. The baseline should be the simpler harness. The second harness and its exact difference are **not chosen yet**; first we need to review recent research and check what can be run with the available computer and budget.

Candidate outcomes:

- Success rate on the first attempt (`pass@1`).
- Success across `k` repeated attempts (`pass^k`; choose and justify `k` in the protocol).
- Cost per successful challenge, number of steps, and elapsed time.
- Failure categories and the share attributable to the harness.

## 4. Decisions still needed before implementation

1. Which agent/model can be run reproducibly, and within what budget?
2. Which CTF challenge suite is legally usable, repeatable, and isolatable?
3. What exactly are the two tool harnesses, and what single component does the ablation remove?
4. What are the run limits, reset procedure, random seeds, and success criteria?

## 5. First code after the protocol is fixed

Build a small experiment runner and log format. Each record should identify the challenge, harness, seed/attempt, success, steps, elapsed time, model usage/cost, and failure category. Pilot the runner on one approved local challenge before the main runs.

## 6. Schedule note

As of 2026-11-14, the November 3 first-results checkpoint has passed. The next checkpoint is November 24 (complete results, ablations, and error analysis), and final submission is December 8. The remaining schedule is tight; prioritize a small, reproducible study and confirm any revised milestone expectations with the course instructor.
