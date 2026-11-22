"""Run the fixed CYB-3 challenge × harness × seed experiment matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from ollama_client import (
    MODEL,
    OLLAMA_TAGS_URL,
    OLLAMA_VERSION_URL,
    ollama_headers,
    validate_ollama_settings,
)
from local_ctf_agent import (
    AGENT_PROMPT_ID,
    CHALLENGES,
    DOCKER_TIMEOUT_SECONDS,
    HARNESS_IDS,
    MAX_AGENT_TURNS,
    MAX_INPUT_CHARS,
    MAX_TOOL_CALLS,
    SYSTEM_PROMPT,
    user_prompt,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 123, 2026)
ORDER_SEED = 20261121


def command_output(arguments: list[str]) -> str:
    """Return a version or image identifier, failing clearly if unavailable."""
    completed = subprocess.run(
        arguments,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=PROJECT_ROOT,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(arguments)}\n{completed.stdout.strip()}")
    return completed.stdout.strip()


def check_ollama() -> dict[str, str]:
    """Confirm the configured Ollama service responds and has the selected model."""
    try:
        validate_ollama_settings()
        request = Request(OLLAMA_TAGS_URL, headers=ollama_headers())
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "The configured Ollama endpoint is not responding; check the endpoint, "
            "tunnel, token, and model service before starting the experiment."
        ) from error
    model_info = next(
        (item for item in payload.get("models", []) if item.get("name") == MODEL),
        None,
    )
    if model_info is None:
        model_names = sorted(item.get("name", "") for item in payload.get("models", []))
        raise RuntimeError(
            f"Model {MODEL!r} is not installed. Models found: {model_names}"
        )
    version_request = Request(OLLAMA_VERSION_URL, headers=ollama_headers())
    try:
        with urlopen(version_request, timeout=15) as response:
            version_payload = json.load(response)
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError("Could not read the Ollama server version.") from error
    return {
        "name": str(model_info.get("name", MODEL)),
        "digest": str(model_info.get("digest", "unavailable")),
        "size": str(model_info.get("size", "unavailable")),
        "server_version": str(version_payload.get("version", "unavailable")),
    }


def make_run_order() -> list[dict[str, str | int]]:
    """Shuffle condition order within challenge/seed blocks reproducibly."""
    rng = random.Random(ORDER_SEED)
    blocks = [
        (challenge_id, seed)
        for challenge_id in CHALLENGES
        for seed in SEEDS
    ]
    rng.shuffle(blocks)
    runs: list[dict[str, str | int]] = []
    for challenge_id, seed in blocks:
        condition_order = list(HARNESS_IDS)
        rng.shuffle(condition_order)
        runs.extend(
            {
                "challenge_id": challenge_id,
                "harness_id": harness_id,
                "seed": seed,
            }
            for harness_id in condition_order
        )
    return runs


def total_memory_bytes() -> int | None:
    """Read total physical memory on POSIX hosts when the OS exposes it."""
    try:
        return int(os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE"))
    except (AttributeError, OSError, ValueError):
        return None


def main() -> int:
    """Preflight, record the frozen matrix, and run every assigned condition."""
    parser = argparse.ArgumentParser(description="Run the frozen CYB-3 experiment matrix.")
    parser.add_argument(
        "--experiment-id",
        default=datetime.now().strftime("main-%Y%m%d"),
        help="Unique output folder label; use a new value for a separate matrix.",
    )
    args = parser.parse_args()
    experiment_id = args.experiment_id
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,63}", experiment_id):
        raise RuntimeError("Experiment ID must contain lowercase letters, digits, and hyphens.")
    output_dir = PROJECT_ROOT / "outputs" / "experiments" / experiment_id
    if output_dir.exists():
        raise RuntimeError(
            f"Output directory already exists: {output_dir.relative_to(PROJECT_ROOT)}. "
            "Choose a new experiment ID before starting another complete matrix."
        )

    protocol_path = PROJECT_ROOT / "EXPERIMENT_PROTOCOL_DRAFT.md"
    protocol_text = protocol_path.read_text(encoding="utf-8")
    status_line = next(
        (line for line in protocol_text.splitlines() if line.startswith("**Status:**")),
        "",
    )
    if not status_line.startswith("**Status:** FROZEN:"):
        parser.error(
            "The protocol is still a draft. Freeze its challenge set, conditions, "
            "metrics, and run order before starting the main matrix."
        )

    model_metadata = check_ollama()
    image_ids = {
        challenge_id: command_output(
            ["docker", "image", "inspect", "--format", "{{.Id}}", challenge["image"]]
        )
        for challenge_id, challenge in CHALLENGES.items()
    }
    ollama_version = model_metadata["server_version"]
    docker_version = command_output(["docker", "--version"])
    run_order = make_run_order()

    config = {
        "experiment_id": experiment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "protocol_status": status_line,
        "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
        "model": MODEL,
        "model_metadata": model_metadata,
        "agent_prompt_id": AGENT_PROMPT_ID,
        "agent_prompts": {
            challenge_id: {
                "system": SYSTEM_PROMPT,
                "user": user_prompt(challenge),
            }
            for challenge_id, challenge in CHALLENGES.items()
        },
        "model_options": {
            "temperature": 0.2,
            "context_tokens": 4096,
            "max_output_tokens": 384,
            "think": False,
        },
        "seeds": list(SEEDS),
        "order_randomization_seed": ORDER_SEED,
        "ollama_version": ollama_version,
        "docker_version": docker_version,
        "host": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "architecture": platform.machine(),
            "cpu_count": os.cpu_count(),
            "total_memory_bytes": total_memory_bytes(),
        },
        "challenge_images": image_ids,
        "conditions": list(HARNESS_IDS),
        "max_agent_turns": MAX_AGENT_TURNS,
        "max_tool_calls": MAX_TOOL_CALLS,
        "max_input_chars": MAX_INPUT_CHARS,
        "docker_timeout_seconds": DOCKER_TIMEOUT_SECONDS,
        "run_count": len(run_order),
        "run_order": run_order,
    }
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "config.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    runner = PROJECT_ROOT / "scripts" / "local_ctf_agent.py"
    relative_output = output_dir.relative_to(PROJECT_ROOT).as_posix()
    failed_invocations = 0
    for index, run in enumerate(run_order, start=1):
        print(
            f"\n[{index}/{len(run_order)}] {run['challenge_id']} / "
            f"{run['harness_id']} / seed {run['seed']}",
            flush=True,
        )
        run_log_path = output_dir / "local_agent_runs.jsonl"
        prior_record_count = (
            len(run_log_path.read_text(encoding="utf-8").splitlines())
            if run_log_path.exists()
            else 0
        )
        result = subprocess.run(
            [
                sys.executable,
                str(runner),
                "--challenge-id",
                str(run["challenge_id"]),
                "--harness",
                str(run["harness_id"]),
                "--seed",
                str(run["seed"]),
                "--output-dir",
                relative_output,
                "--study-id",
                experiment_id,
            ],
            check=False,
            cwd=PROJECT_ROOT,
        )
        records = (
            run_log_path.read_text(encoding="utf-8").splitlines()
            if run_log_path.exists()
            else []
        )
        if len(records) <= prior_record_count:
            print("Runner produced no run record; stopping the matrix.", flush=True)
            return 2
        latest_record = json.loads(records[-1])
        if latest_record.get("status") == "incomplete":
            print(
                "Infrastructure failure recorded. Stopping the matrix here; "
                "do not count this run as an agent failure.",
                flush=True,
            )
            return 2
        if result.returncode not in (0, 1):
            failed_invocations += 1
            print(f"Runner invocation ended with code {result.returncode}.", flush=True)

    print(
        f"\nMatrix finished: {len(run_order)} runs; "
        f"runner-level errors={failed_invocations}; "
        f"records={relative_output}/local_agent_runs.jsonl",
        flush=True,
    )
    return 0 if failed_invocations == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
