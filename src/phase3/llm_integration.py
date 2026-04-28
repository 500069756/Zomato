from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests


def load_groq_api_key(env_path: Path | str = ".env") -> str | None:
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key and api_key.strip() not in {"your_actual_groq_api_key_here", "REPLACE_ME", ""}:
        return api_key.strip()

    def read_env(path: Path) -> str | None:
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as env_file:
            for line in env_file:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "GROQ_API_KEY" in stripped:
                    key = stripped.split("=", 1)[1].strip().strip('"').strip("'")
                    if key and key not in {"your_actual_groq_api_key_here", "REPLACE_ME", ""}:
                        return key
        return None

    env_path = Path(env_path)
    root_key = read_env(env_path)
    if root_key:
        return root_key

    module_env = Path(__file__).resolve().parent / ".env"
    return read_env(module_env)


def build_groq_prompt(candidates: list[dict[str, Any]], user_preferences: dict[str, Any]) -> str:
    prompt_lines = [
        "You are an AI assistant that ranks restaurant recommendations.",
        "Use the user preferences and candidate restaurant data to choose the best options.",
        "Provide a ranked list with a short explanation for each.",
        "",
        "User preferences:",
    ]

    for key, value in user_preferences.items():
        prompt_lines.append(f"- {key}: {value}")

    prompt_lines.append("")
    prompt_lines.append("Candidate restaurants:")

    for candidate in candidates:
        prompt_lines.append(
            f"- {candidate.get('restaurant_name')} | {candidate.get('primary_cuisine')} | "
            f"Rating: {candidate.get('rating')} | Budget: {candidate.get('budget_label')} | "
            f"Location: {candidate.get('location')}"
        )

    prompt_lines.append("")
    prompt_lines.append("Explain why each restaurant is a good fit and provide a final recommendation summary.")
    return "\n".join(prompt_lines)


def call_groq_llm(prompt: str, model: str = "openai/gpt-oss-20b", max_output_tokens: int = 256) -> str:
    api_key = load_groq_api_key()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment or .env file")

    url = "https://api.groq.com/openai/v1/responses"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "input": prompt,
        "max_output_tokens": max_output_tokens,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return parse_groq_response(result)
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise RuntimeError(f"Groq API authentication failed (401). Please check your API key. Details: {e}")
        elif response.status_code == 429:
            raise RuntimeError(f"Groq API rate limit exceeded (429). Please try again later. Details: {e}")
        else:
            raise RuntimeError(f"Groq API error ({response.status_code}): {e}")
    except requests.exceptions.Timeout:
        raise RuntimeError("Groq API request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Groq API request failed: {e}")


def parse_groq_response(response_json: dict[str, Any]) -> str:
    if "output_text" in response_json and response_json["output_text"]:
        return response_json["output_text"].strip()

    output = response_json.get("output")
    if isinstance(output, list):
        pieces: list[str] = []
        for item in output:
            if isinstance(item, dict):
                content = item.get("content")
                if isinstance(content, list):
                    for chunk in content:
                        if isinstance(chunk, dict) and "text" in chunk:
                            pieces.append(str(chunk["text"]))
                        elif isinstance(chunk, str):
                            pieces.append(chunk)
                elif isinstance(content, str):
                    pieces.append(content)
                elif "text" in item:
                    pieces.append(str(item["text"]))
        result = "".join(pieces).strip()
        if result:
            return result

    if isinstance(response_json, dict):
        return str(response_json)

    return ""
