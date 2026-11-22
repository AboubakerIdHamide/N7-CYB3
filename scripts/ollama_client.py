"""Shared connection settings for the project's Ollama-compatible model API."""

from __future__ import annotations

import os
from urllib.parse import urlsplit


DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_BASE_URL = os.environ.get("CYB3_OLLAMA_URL", DEFAULT_OLLAMA_URL).rstrip("/")
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"
OLLAMA_VERSION_URL = f"{OLLAMA_BASE_URL}/api/version"
MODEL = os.environ.get("CYB3_OLLAMA_MODEL", "qwen3.5:4b")
_OLLAMA_TOKEN = os.environ.get("CYB3_OLLAMA_TOKEN", "")


def validate_ollama_settings() -> None:
    """Reject unsafe or malformed remote endpoints before sending credentials."""
    parsed = urlsplit(OLLAMA_BASE_URL)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise RuntimeError("CYB3_OLLAMA_URL must be an HTTP(S) base URL.")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise RuntimeError(
            "CYB3_OLLAMA_URL must not contain credentials, a query, or a fragment."
        )

    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if parsed.hostname not in local_hosts:
        if parsed.scheme != "https":
            raise RuntimeError("Remote Ollama endpoints must use HTTPS.")
        if not _OLLAMA_TOKEN:
            raise RuntimeError(
                "Set CYB3_OLLAMA_TOKEN when using a remote Ollama endpoint."
            )


def ollama_headers(*, json_body: bool = False) -> dict[str, str]:
    """Build request headers without putting the access token in a URL or log."""
    headers: dict[str, str] = {}
    if json_body:
        headers["Content-Type"] = "application/json"
    if _OLLAMA_TOKEN:
        headers["Authorization"] = f"Bearer {_OLLAMA_TOKEN}"
    return headers
