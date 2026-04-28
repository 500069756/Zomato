from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.phase2.recommend import recommend
from src.phase3.llm_integration import build_groq_prompt, call_groq_llm, load_groq_api_key
from src.phase4.recommendation_engine import build_recommendation_response, response_to_dict


app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS for all routes


def parse_preferences(json_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "location": json_data.get("location") or None,
        "budget": json_data.get("budget") or None,
        "cuisine": json_data.get("cuisine") or None,
        "minimum_rating": float(json_data.get("minimum_rating") or 0.0),
        "additional_preferences": [
            pref.strip()
            for pref in (json_data.get("additional_preferences") or "").split(",")
            if pref.strip()
        ],
        "top_n": int(json_data.get("top_n") or 5),
    }


def assign_explanations(text: str, candidates: list[dict[str, Any]]) -> dict[str, str]:
    if not text:
        return {}

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    explanations: dict[str, str] = {}

    for candidate in candidates:
        name = candidate.get("restaurant_name", "")
        lower_name = name.lower()
        matched = next((line for line in lines if lower_name and lower_name in line.lower()), None)
        explanations[name] = matched or text.strip()

    return explanations


def call_llm_for_candidates(candidates: list[dict[str, Any]], user_preferences: dict[str, Any]) -> tuple[dict[str, str], str | None]:
    if not load_groq_api_key():
        return {}, "Groq API key not configured."

    prompt = build_groq_prompt(candidates, user_preferences)
    try:
        response_text = call_groq_llm(prompt, model="openai/gpt-oss-20b", max_output_tokens=220)
        return assign_explanations(response_text, candidates), None
    except Exception as exc:
        return {}, str(exc)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok"})


@app.route("/api/localities", methods=["GET"])
def get_localities() -> Any:
    try:
        df = pd.read_csv("src/phase1/data/processed/clean_zomato_restaurants.csv")
        localities = df['location'].unique().tolist()
        localities = sorted([loc for loc in localities if loc and str(loc).strip()])
        return jsonify({"localities": localities})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/recommend", methods=["POST"])
def api_recommend() -> Any:
    request_data = request.get_json(silent=True) or {}
    user_preferences = parse_preferences(request_data)

    try:
        candidates = recommend(
            dataset_path="src/phase1/data/processed/clean_zomato_restaurants.csv",
            location=user_preferences["location"],
            budget=user_preferences["budget"],
            cuisine=user_preferences["cuisine"],
            minimum_rating=user_preferences["minimum_rating"],
            additional_preferences=user_preferences["additional_preferences"],
            top_n=user_preferences["top_n"],
        )
    except Exception as exc:
        return jsonify(
            {
                "success": False,
                "summary": "Unable to load candidate recommendations.",
                "recommendations": [],
                "fallback_message": str(exc),
                "analytics": {"error": str(exc)},
            }
        ), 500

    llm_explanations, llm_error = call_llm_for_candidates(candidates, user_preferences)

    response = build_recommendation_response(
        candidates=candidates,
        llm_explanations=llm_explanations,
        user_preferences=user_preferences,
        analytics={"llm_error": llm_error} if llm_error else None,
    )

    payload = response_to_dict(response)
    if llm_error:
        payload["warning"] = str(llm_error)

    return jsonify(payload)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
