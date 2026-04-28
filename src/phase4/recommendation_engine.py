from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FormattedRecommendation:
    restaurant_name: str
    location: str
    cuisine: str
    rating: float
    budget_label: str
    explanation: str
    address: str | None = None
    cuisine_tags: list[str] | None = None


@dataclass
class RecommendationResponse:
    success: bool
    recommendations: list[FormattedRecommendation]
    summary: str
    fallback_message: str | None = None
    analytics: dict[str, Any] | None = None


def merge_candidate_with_llm_explanation(
    candidate: dict[str, Any],
    llm_explanations: dict[str, str],
) -> FormattedRecommendation | None:
    """Merge a Phase 2 candidate with LLM explanation from Phase 3."""
    restaurant_name = candidate.get("restaurant_name")
    if not restaurant_name:
        return None

    explanation = llm_explanations.get(restaurant_name, "")
    return FormattedRecommendation(
        restaurant_name=restaurant_name,
        location=candidate.get("location", "Unknown"),
        cuisine=candidate.get("primary_cuisine", "Other"),
        rating=float(candidate.get("rating", 0.0)),
        budget_label=candidate.get("budget_label", "unknown"),
        explanation=explanation,
        address=candidate.get("address"),
        cuisine_tags=candidate.get("cuisine_tags", []),
    )


def build_recommendation_response(
    candidates: list[dict[str, Any]],
    llm_explanations: dict[str, str],
    user_preferences: dict[str, Any],
    analytics: dict[str, Any] | None = None,
) -> RecommendationResponse:
    """Build the final recommendation response combining Phase 2 and Phase 3 outputs."""
    if not candidates:
        fallback_msg = _generate_fallback_message(user_preferences)
        return RecommendationResponse(
            success=False,
            recommendations=[],
            summary=fallback_msg,
            fallback_message=fallback_msg,
            analytics=analytics,
        )

    formatted_recommendations = []
    for candidate in candidates:
        formatted = merge_candidate_with_llm_explanation(candidate, llm_explanations)
        if formatted:
            formatted_recommendations.append(formatted)

    if not formatted_recommendations:
        fallback_msg = _generate_fallback_message(user_preferences)
        return RecommendationResponse(
            success=False,
            recommendations=[],
            summary=fallback_msg,
            fallback_message=fallback_msg,
            analytics=analytics,
        )

    summary = _generate_summary(formatted_recommendations, user_preferences)

    return RecommendationResponse(
        success=True,
        recommendations=formatted_recommendations,
        summary=summary,
        fallback_message=None,
        analytics=analytics,
    )


def _generate_summary(recommendations: list[FormattedRecommendation], user_preferences: dict[str, Any]) -> str:
    """Generate a user-facing summary of recommendations."""
    if not recommendations:
        return "No recommendations found."

    top_rec = recommendations[0]
    location_pref = user_preferences.get("location", "any location")
    cuisine_pref = user_preferences.get("cuisine", "any cuisine")
    budget_pref = user_preferences.get("budget", "any budget")

    summary_parts = [
        f"Based on your preferences for {cuisine_pref} cuisine in {location_pref} with {budget_pref} budget,",
        f"we recommend '{top_rec.restaurant_name}' as the top choice.",
        f"It has a rating of {top_rec.rating} and offers {top_rec.cuisine} cuisine.",
    ]

    if len(recommendations) > 1:
        summary_parts.append(f"We also found {len(recommendations) - 1} other great options for you.")

    return " ".join(summary_parts)


def _generate_fallback_message(user_preferences: dict[str, Any]) -> str:
    """Generate a fallback message when no matches are found."""
    suggestions = []

    if user_preferences.get("budget"):
        suggestions.append("relaxing your budget constraint")

    if user_preferences.get("minimum_rating", 0.0) > 0:
        suggestions.append("lowering the minimum rating requirement")

    if user_preferences.get("cuisine"):
        suggestions.append("exploring alternative cuisines")

    if user_preferences.get("location"):
        suggestions.append("searching in nearby areas")

    if suggestions:
        return (
            f"No restaurants match all your criteria. "
            f"Consider {', or '.join(suggestions)} to see more options."
        )
    return "No restaurants found matching your preferences."


def to_dict(recommendation: FormattedRecommendation) -> dict[str, Any]:
    """Convert a FormattedRecommendation to a dictionary for serialization."""
    return {
        "restaurant_name": recommendation.restaurant_name,
        "location": recommendation.location,
        "cuisine": recommendation.cuisine,
        "rating": recommendation.rating,
        "budget_label": recommendation.budget_label,
        "explanation": recommendation.explanation,
        "address": recommendation.address,
        "cuisine_tags": recommendation.cuisine_tags or [],
    }


def response_to_dict(response: RecommendationResponse) -> dict[str, Any]:
    """Convert a RecommendationResponse to a dictionary for JSON serialization."""
    return {
        "success": response.success,
        "recommendations": [to_dict(rec) for rec in response.recommendations],
        "summary": response.summary,
        "fallback_message": response.fallback_message,
        "analytics": response.analytics or {},
    }
