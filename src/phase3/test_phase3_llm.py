from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.phase3.llm_integration import (
    build_groq_prompt,
    call_groq_llm,
    load_groq_api_key,
)


def test_api_key_loading() -> None:
    print("=" * 70)
    print("TEST 1: API Key Loading")
    print("=" * 70)
    api_key = load_groq_api_key()
    print(f"API key found: {bool(api_key)}")
    if api_key:
        print("API key loaded successfully.")
    else:
        print("No API key found. Please set GROQ_API_KEY in .env or environment variables.")
    assert api_key is not None, "GROQ_API_KEY must be available for live tests"
    print("\nTest 1 PASSED\n")


def test_small_prompt_call() -> None:
    print("=" * 70)
    print("TEST 2: Small Groq LLM Prompt Call")
    print("=" * 70)

    prompt = "Please provide a short friendly greeting in one sentence."
    response = call_groq_llm(prompt, model="openai/gpt-oss-20b", max_output_tokens=50)
    print(f"Response: {response}")
    assert response and len(response.strip()) > 0, "LLM must return a non-empty response"
    print("\nTest 2 PASSED\n")


def test_recommendation_prompt_call() -> None:
    print("=" * 70)
    print("TEST 3: Recommendation Prompt Call")
    print("=" * 70)

    candidates = [
        {
            "restaurant_name": "Ocean Breeze Bistro",
            "primary_cuisine": "Seafood",
            "rating": 4.6,
            "budget_label": "high",
            "location": "Bangalore",
        },
        {
            "restaurant_name": "Little Italy Cafe",
            "primary_cuisine": "Italian",
            "rating": 4.2,
            "budget_label": "medium",
            "location": "Bangalore",
        },
    ]
    user_preferences = {
        "location": "Bangalore",
        "budget": "medium",
        "cuisine": "Seafood",
        "minimum_rating": 4.0,
    }

    prompt = build_groq_prompt(candidates, user_preferences)
    response = call_groq_llm(prompt, model="openai/gpt-oss-20b", max_output_tokens=180)
    print(f"Response: {response}")
    assert response and "recommend" in response.lower(), "LLM response should contain recommendation text"
    print("\nTest 3 PASSED\n")


if __name__ == "__main__":
    test_api_key_loading()
    test_small_prompt_call()
    test_recommendation_prompt_call()
    print("=" * 70)
    print("ALL PHASE 3 LLM TESTS COMPLETE")
    print("=" * 70)
