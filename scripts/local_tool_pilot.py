"""Run a harmless local Ollama tool-call pilot using only a calculator tool."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from ollama_client import (
    MODEL,
    OLLAMA_CHAT_URL,
    ollama_headers,
    validate_ollama_settings,
)


# Ollama reads this schema to know which tool the model may request.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two integers and return their sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
        },
    }
]


def chat(messages: list[dict[str, object]], *, tools: list[dict[str, object]] | None = None) -> dict:
    """Send chat history and optional tool descriptions to local Ollama."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": tools or [],
        "stream": False,
        "think": False,
        "options": {"num_ctx": 2048, "num_predict": 64},
    }
    request = Request(
        OLLAMA_CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=ollama_headers(json_body=True),
        method="POST",
    )
    try:
        validate_ollama_settings()
        with urlopen(request, timeout=300) as response:
            return json.load(response)
    except URLError as error:
        raise RuntimeError(
            f"Cannot reach the configured Ollama endpoint for model {MODEL!r}. "
            "Check the endpoint, tunnel, and model service."
        ) from error


def main() -> None:
    """Demonstrate one safe model request, local tool call, and follow-up."""
    messages: list[dict[str, object]] = [
        {
            "role": "user",
            "content": "Use the add_numbers tool to calculate 23 plus 19, then tell me the result.",
        }
    ]

    first_response = chat(messages, tools=TOOLS)
    assistant_message = first_response.get("message", {})
    tool_calls = assistant_message.get("tool_calls", [])
    if len(tool_calls) != 1:
        raise RuntimeError(
            f"Expected exactly one add_numbers tool call, got: {assistant_message!r}"
        )

    tool_call = tool_calls[0]
    function = tool_call.get("function", {})
    if function.get("name") != "add_numbers":
        raise RuntimeError(f"Refusing unapproved tool: {function.get('name')!r}")

    arguments = function.get("arguments", {})
    a, b = arguments.get("a"), arguments.get("b")
    if type(a) is not int or type(b) is not int:
        raise RuntimeError(f"Expected integer arguments, got: {arguments!r}")

    result = a + b
    # Give Ollama both its original tool request and the calculator's reply.
    messages.extend(
        [
            assistant_message,
            {
                "role": "tool",
                "tool_name": "add_numbers",
                "content": str(result),
            },
        ]
    )
    final_response = chat(messages)
    final_message = final_response.get("message", {})

    print(f"Model: {MODEL}")
    print(f"Tool call: add_numbers(a={a}, b={b})")
    print(f"Tool result: {result}")
    print(f"Model final answer: {final_message.get('content', '').strip()}")


if __name__ == "__main__":
    main()
