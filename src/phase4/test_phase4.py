from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.phase4.recommendation_engine import (
    FormattedRecommendation,
    build_recommendation_response,
    response_to_dict,
)


def test_case_1_successful_recommendation() -> None:
    """Test Case 1: Successfully merge candidates with LLM explanations."""
    print("=" * 70)
    print("TEST CASE 1: Successful Recommendation Merge")
    print("=" * 70)

    candidates = [
        {
            "restaurant_name": "Delhi Spice House",
            "location": "Delhi",
            "primary_cuisine": "North Indian",
            "cuisine_tags": ["North Indian", "Vegetarian"],
            "rating": 4.5,
            "budget_label": "medium",
            "votes": 250,
            "address": "Connaught Place, Delhi",
            "score": 85.3,
        },
        {
            "restaurant_name": "Mughlai Delight",
            "location": "Delhi",
            "primary_cuisine": "North Indian",
            "cuisine_tags": ["North Indian", "Non-Vegetarian"],
            "rating": 4.3,
            "budget_label": "medium",
            "votes": 180,
            "address": "Karol Bagh, Delhi",
            "score": 78.9,
        },
    ]

    llm_explanations = {
        "Delhi Spice House": "Perfect for your medium budget with excellent North Indian cuisine. Highly rated and family-friendly.",
        "Mughlai Delight": "Great option for authentic Mughlai flavors at reasonable prices. Good reviews and convenient location.",
    }

    user_preferences = {
        "location": "Delhi",
        "budget": "medium",
        "cuisine": "North Indian",
        "minimum_rating": 4.0,
    }

    response = build_recommendation_response(candidates, llm_explanations, user_preferences)
    result = response_to_dict(response)

    print(f"Success: {result['success']}")
    print(f"Summary: {result['summary']}")
    print(f"Recommendations Count: {len(result['recommendations'])}")
    for idx, rec in enumerate(result['recommendations'], 1):
        print(f"\n  {idx}. {rec['restaurant_name']}")
        print(f"     Location: {rec['location']}")
        print(f"     Cuisine: {rec['cuisine']}")
        print(f"     Rating: {rec['rating']}")
        print(f"     Budget: {rec['budget_label']}")
        print(f"     Explanation: {rec['explanation']}")

    assert result['success'] is True, "Response should be successful"
    assert len(result['recommendations']) == 2, "Should have 2 recommendations"
    assert result['fallback_message'] is None, "No fallback message for successful case"
    print("\n✅ Test Case 1 PASSED\n")


def test_case_2_empty_candidates() -> None:
    """Test Case 2: Handle empty candidates with fallback message."""
    print("=" * 70)
    print("TEST CASE 2: No Matching Restaurants (Fallback)")
    print("=" * 70)

    candidates = []
    llm_explanations = {}

    user_preferences = {
        "location": "Delhi",
        "budget": "low",
        "cuisine": "Japanese",
        "minimum_rating": 4.8,
    }

    response = build_recommendation_response(candidates, llm_explanations, user_preferences)
    result = response_to_dict(response)

    print(f"Success: {result['success']}")
    print(f"Summary: {result['summary']}")
    print(f"Fallback Message: {result['fallback_message']}")
    print(f"Recommendations Count: {len(result['recommendations'])}")

    assert result['success'] is False, "Response should not be successful"
    assert len(result['recommendations']) == 0, "Should have 0 recommendations"
    assert result['fallback_message'] is not None, "Fallback message should be present"
    print("\n✅ Test Case 2 PASSED\n")


def test_case_3_mixed_budget() -> None:
    """Test Case 3: Multiple recommendations with different cuisines."""
    print("=" * 70)
    print("TEST CASE 3: Multiple Cuisines and Budget Levels")
    print("=" * 70)

    candidates = [
        {
            "restaurant_name": "China Town Express",
            "location": "Bangalore",
            "primary_cuisine": "Chinese",
            "cuisine_tags": ["Chinese", "Asian"],
            "rating": 4.1,
            "budget_label": "low",
            "votes": 120,
            "address": "Indiranagar, Bangalore",
            "score": 72.4,
        },
        {
            "restaurant_name": "Italian Nights",
            "location": "Bangalore",
            "primary_cuisine": "Italian",
            "cuisine_tags": ["Italian", "Continental"],
            "rating": 4.4,
            "budget_label": "high",
            "votes": 95,
            "address": "Whitefield, Bangalore",
            "score": 68.2,
        },
    ]

    llm_explanations = {
        "China Town Express": "Budget-friendly Chinese restaurant with good ratings and quick service.",
        "Italian Nights": "Premium Italian dining experience with authentic recipes and excellent ambiance.",
    }

    user_preferences = {
        "location": "Bangalore",
        "budget": None,
        "cuisine": None,
        "minimum_rating": 4.0,
    }

    response = build_recommendation_response(candidates, llm_explanations, user_preferences)
    result = response_to_dict(response)

    print(f"Success: {result['success']}")
    print(f"Summary: {result['summary']}")
    print(f"Recommendations Count: {len(result['recommendations'])}")
    for idx, rec in enumerate(result['recommendations'], 1):
        print(f"\n  {idx}. {rec['restaurant_name']}")
        print(f"     Cuisine: {rec['cuisine']}")
        print(f"     Budget: {rec['budget_label']}")
        print(f"     Explanation: {rec['explanation']}")

    assert result['success'] is True, "Response should be successful"
    assert len(result['recommendations']) == 2, "Should have 2 recommendations"
    print("\n✅ Test Case 3 PASSED\n")


if __name__ == "__main__":
    test_case_1_successful_recommendation()
    test_case_2_empty_candidates()
    test_case_3_mixed_budget()
    print("=" * 70)
    print("ALL TESTS PASSED ✅")
    print("=" * 70)
