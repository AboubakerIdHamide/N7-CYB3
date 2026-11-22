"""Model-independent JSONL logging for CYB-3 experiment runs."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


RunStatus = Literal["success", "failure", "incomplete"]


@dataclass(frozen=True, slots=True)
class RunRecord:
    """One agent attempt on one challenge under one harness."""

    challenge_id: str
    harness_id: str
    attempt: int
    seed: int | str
    status: RunStatus
    model_id: str
    started_at: str
    finished_at: str
    steps: int
    elapsed_seconds: float
    agent_prompt_id: str | None = None
    study_id: str | None = None
    cost_usd: float | None = None
    api_cost_usd: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    failure_category: str | None = None
    failure_events: tuple[str, ...] = ()
    trace_path: str | None = None

    def __post_init__(self) -> None:
        """Reject invalid run data as soon as a record is created."""
        if not self.challenge_id.strip():
            raise ValueError("challenge_id must not be empty")
        if not self.harness_id.strip():
            raise ValueError("harness_id must not be empty")
        if not self.model_id.strip():
            raise ValueError("model_id must not be empty")
        if self.attempt < 1:
            raise ValueError("attempt must be at least 1")
        if self.steps < 0:
            raise ValueError("steps must not be negative")
        if self.elapsed_seconds < 0:
            raise ValueError("elapsed_seconds must not be negative")
        if self.cost_usd is not None and self.cost_usd < 0:
            raise ValueError("cost_usd must not be negative")
        # Token counts are optional, but any recorded count must be non-negative.
        for name, value in (
            ("input_tokens", self.input_tokens),
            ("output_tokens", self.output_tokens),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{name} must not be negative")

    @classmethod
    def now_iso(cls) -> str:
        """Return a timezone-aware UTC timestamp for run boundaries."""
        return datetime.now(timezone.utc).isoformat()


def append_run(record: RunRecord, path: str | Path) -> None:
    """Append one validated record as a JSON object followed by a newline."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as stream:
        # Convert the dataclass fields into a plain dictionary before JSON encoding.
        stream.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
