"""
AI Code Review helper using GitHub Models (openai/gpt-4o-mini).

This module can be used locally or integrated into other tools
to perform AI-based code review on a given diff string.

It expects a GitHub Models PAT to be available in the environment,
typically the same one used in the CI workflow.

Required environment variables:
- GITHUB_TOKEN: Personal Access Token with `models:read` permission.

Example usage (from a terminal):

    export GITHUB_TOKEN=<your_pat_here>
    python -m bot.review pr_diff.txt

If you call review_diff() directly, just pass the diff as a string.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Optional

import requests


GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference/chat/completions"
DEFAULT_MODEL = "openai/gpt-4o-mini"


class AIReviewError(Exception):
    """Custom exception for AI review related errors."""


def build_prompt(diff_text: str) -> str:
    """
    Build the prompt sent to the LLM from the raw diff.

    :param diff_text: Git diff of a pull request.
    :return: Prompt string.
    """
    return f"""
You are an expert senior code and content reviewer.
You receive a unified Git diff. Your tasks are:

1. *Change Overview (what changed vs previous version)*
- Provide a concise bullet list of the main changes.
- For each item, mention the file name and a short description.
- Example: file.txt – new text file added containing a personal message.

2. *Detailed Diff Explanation (before vs after)*
- For each file in the diff, explain what changed compared to the previous version:
    - What was added?
    - What was removed?
    - What was modified?
- When useful, quote small snippets (in backticks) to show the old vs new behavior.

3. *Quality, Risks & Sensitive Content*
- Highlight bugs, logic issues, readability problems, and code smells.
- Analyze configuration and text files as well, not only source code.
- Explicitly flag any *personal, sensitive or inappropriate content* that should not be committed (e.g. names, private messages, secrets).
- Mention potential security or privacy risks.

4. *Actionable Recommendations*
- Provide practical suggestions to improve the changes.
- You can propose refactors, better naming, extra tests, or removal of sensitive data.

Respond in clear Markdown with the following sections:

- Summary of Changes
- File-by-file Diff Explanation
- Risks & Sensitive Content
- Recommendations

Diff:
{diff_text}
""".strip()


def review_diff(
    diff_text: str,
    model: str = DEFAULT_MODEL,
    token: Optional[str] = None,
) -> str:
    """
    Call GitHub Models to review a given diff.

    :param diff_text: Git diff as a string.
    :param model: Model name, default is openai/gpt-4o-mini.
    :param token: GitHub Models PAT (if None, read from env GITHUB_TOKEN).
    :return: AI-generated review text.
    :raises AIReviewError: On missing token or HTTP/API errors.
    """
    if not diff_text.strip():
        raise AIReviewError("Empty diff provided; nothing to review.")

    if token is None:
        token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise AIReviewError(
            "Missing GITHUB_TOKEN environment variable. "
            "Set it to a GitHub PAT with models:read permissions."
        )

    prompt = build_prompt(diff_text)

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        response = requests.post(
            GITHUB_MODELS_ENDPOINT,
            headers=headers,
            data=json.dumps(payload),
            timeout=60,
        )
    except requests.RequestException as exc:
        raise AIReviewError(f"HTTP request failed: {exc}") from exc

    if response.status_code != 200:
        raise AIReviewError(
            f"GitHub Models API returned {response.status_code}: {response.text}"
        )

    data = response.json()

    # The SDK sample uses: response.body.choices[0].message.content
    # Here we handle both string and list-of-parts formats defensively.
    try:
        message_content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise AIReviewError(
            f"Unexpected response format from API: {json.dumps(data, indent=2)}"
        ) from exc

    if isinstance(message_content, str):
        return message_content

    # Some formats may return a list of content parts
    if isinstance(message_content, list):
        # Join any 'text' fields if present, otherwise cast to string
        parts = []
        for part in message_content:
            if isinstance(part, dict) and "text" in part:
                parts.append(str(part["text"]))
            else:
                parts.append(str(part))
        return "\n".join(parts)

    # Fallback: just stringify whatever it is
    return str(message_content)


def _read_file(path: str) -> str:
    """Utility to read a text file using UTF-8."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main(argv: list[str]) -> int:
    """
    Simple CLI entrypoint.

    Usage:
        python -m bot.review path/to/diff.txt

    The result will be printed to stdout.
    """
    if len(argv) < 2:
        print("Usage: python -m bot.review path/to/diff.txt", file=sys.stderr)
        return 1

    diff_path = argv[1]
    try:
        diff_text = _read_file(diff_path)
    except OSError as exc:
        print(f"Error reading diff file '{diff_path}': {exc}", file=sys.stderr)
        return 1

    try:
        review = review_diff(diff_text)
    except AIReviewError as exc:
        print(f"AI review failed: {exc}", file=sys.stderr)
        return 2

    print(review)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))