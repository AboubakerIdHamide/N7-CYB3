# Ollama preflight launch failures

| Field | Value |
|---|---|
| Date | 2026-11-21 (UTC) |
| Intended challenge | `local_buffer_overflow_0` |
| Intended model | `qwen3:1.7b` |
| Attempt field emitted | 3 |
| Actions / duration | 0 / 0.029 and 0.017 seconds |
| Result | Incomplete: Ollama was unreachable at `127.0.0.1:11434` |

Two launches stopped before requesting a model response or invoking the challenge container. These are environment startup failures, not evidence about the agent's ability to solve the challenge. They do not consume completed challenge-attempt numbers; the subsequent valid run is labeled attempt 3.

The emitted records refer to trace paths that were not created by the older runner because it only wrote traces after its first successful model response. The runner was later updated to write a `run_started` trace event before contacting Ollama and a `runner_error` event when startup fails.

## Saved evidence

- `2026-11-21-preflight-launch-failure-run.jsonl` — both incomplete run records as emitted.
- No trace files were created for these launches; the nonexistent paths are retained in the raw run records.
