from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


BUDGET_CATEGORIES = {"low", "medium", "high"}


@dataclass(frozen=True)
class UserPreferences:
    location: str | None = None
    budget: str | None = None
    cuisine: str | None = None
    minimum_rating: float = 0.0
    additional_preferences: list[str] = None

    def __post_init__(self) -> None:
        # Safely convert location to title case
        if self.location and isinstance(self.location, str):
            object.__setattr__(self, "location", self.location.strip().title())
        else:
            object.__setattr__(self, "location", None)
        
        # Safely convert budget to lowercase
        if self.budget and isinstance(self.budget, str):
            object.__setattr__(self, "budget", self.budget.strip().lower())
        else:
            object.__setattr__(self, "budget", None)
        
        # Safely convert cuisine to title case
        if self.cuisine and isinstance(self.cuisine, str):
            object.__setattr__(self, "cuisine", self.cuisine.strip().title())
        else:
            object.__setattr__(self, "cuisine", None)
        
        # Convert minimum_rating to float
        object.__setattr__(self, "minimum_rating", float(self.minimum_rating) if self.minimum_rating is not None else 0.0)
        
        # Safely convert additional_preferences to lowercase list
        if self.additional_preferences and isinstance(self.additional_preferences, list):
            object.__setattr__(self, "additional_preferences", [
                pref.strip().lower() for pref in self.additional_preferences if isinstance(pref, str) and pref.strip()
            ])
        else:
            object.__setattr__(self, "additional_preferences", [])


def load_clean_data(dataset_path: Path | str = "src/phase1/data/processed/clean_zomato_restaurants.csv") -> pd.DataFrame:
    dataset_path = Path(dataset_path)
    if dataset_path.suffix == ".parquet":
        frame = pd.read_parquet(dataset_path)
    else:
        frame = pd.read_csv(dataset_path)

    frame["location"] = frame["location"].astype(str).str.strip()
    frame["budget_label"] = frame["budget_label"].astype(str).str.lower().replace({"nan": ""})
    frame["rating"] = pd.to_numeric(frame["rating"], errors="coerce").fillna(0.0)
    frame["votes"] = pd.to_numeric(frame["votes"], errors="coerce").fillna(0).astype(int)
    
    # Handle cuisine_tags parsing - handle both string representations and actual lists
    def parse_cuisine_tags(value):
        if isinstance(value, list):
            return value
        if isinstance(value, str) and value.startswith("["):
            try:
                import ast
                return ast.literal_eval(value)
            except:
                return []
        return []
    
    frame["cuisine_tags"] = frame["cuisine_tags"].apply(parse_cuisine_tags)
    return frame


def normalize_text(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip()
    return text if text else None


def matches_location(record_location: str, preferred_location: str) -> bool:
    if not preferred_location:
        return True
    if not record_location or not isinstance(record_location, str):
        return False
    return preferred_location.lower() == record_location.lower() or preferred_location.lower() in record_location.lower()


def matches_budget(record_budget: str, preferred_budget: str) -> bool:
    if not preferred_budget:
        return True
    if not record_budget or not isinstance(record_budget, str):
        return False
    return record_budget.lower() == preferred_budget.lower()


def matches_cuisine(cuisine_tags: list[str], preferred_cuisine: str) -> bool:
    if not preferred_cuisine:
        return True
    normalized_preference = preferred_cuisine.title()
    return normalized_preference in cuisine_tags or any(normalized_preference in tag for tag in cuisine_tags)


def matches_additional_preferences(record: pd.Series, preferences: list[str]) -> int:
    if not preferences:
        return 0

    text_fields = [
        normalize_text(record.get("restaurant_name")) or "",
        normalize_text(record.get("primary_cuisine")) or "",
        normalize_text(record.get("address")) or "",
    ]
    haystack = " ".join(text_fields).lower()
    return sum(1 for pref in preferences if pref in haystack)


def compute_score(record: pd.Series, prefs: UserPreferences) -> float:
    score = 0.0

    # Location match (highest priority)
    if prefs.location and matches_location(record["location"], prefs.location):
        score += 25.0

    # Budget match
    if prefs.budget and matches_budget(record["budget_label"], prefs.budget):
        score += 20.0
    elif prefs.budget and record["budget_label"]:
        score += 5.0

    # Cuisine match (very important)
    if prefs.cuisine and matches_cuisine(record["cuisine_tags"], prefs.cuisine):
        score += 30.0

    # Rating component (only if rating data is available)
    rating_value = float(record["rating"] or 0.0)
    if rating_value > 0:
        score += rating_value * 8.0
    
    # Votes component (indicates popularity)
    votes_value = int(record["votes"] or 0)
    if votes_value > 0:
        score += min(math.log1p(votes_value), 5.0)
    
    # Additional preferences
    score += matches_additional_preferences(record, prefs.additional_preferences) * 3.0

    return score


def filter_restaurants(
    df: pd.DataFrame,
    prefs: UserPreferences,
    top_n: int = 10,
) -> pd.DataFrame:
    filtered = df.copy()

    # Ensure required columns exist
    required_cols = ['restaurant_name', 'location', 'budget_label', 'cuisine_tags', 'rating', 'votes']
    for col in required_cols:
        if col not in filtered.columns:
            raise ValueError(f"Required column '{col}' not found in dataset. Available columns: {list(filtered.columns)}")

    # Apply location filter
    if prefs.location:
        filtered = filtered[filtered["location"].apply(lambda loc: matches_location(loc, prefs.location))]

    # Apply budget filter
    if prefs.budget:
        budget_filtered = filtered[filtered["budget_label"].apply(lambda value: matches_budget(value, prefs.budget))]
        # Only use budget filter if it returns results
        if not budget_filtered.empty:
            filtered = budget_filtered

    # Apply cuisine filter
    if prefs.cuisine:
        cuisine_filtered = filtered[filtered["cuisine_tags"].apply(lambda tags: matches_cuisine(tags, prefs.cuisine))]
        # Only use cuisine filter if it returns results
        if not cuisine_filtered.empty:
            filtered = cuisine_filtered

    # Apply rating filter
    if prefs.minimum_rating > 0.0:
        filtered["rating"] = pd.to_numeric(filtered["rating"], errors="coerce").fillna(0.0)
        rating_filtered = filtered[filtered["rating"] >= prefs.minimum_rating]
        # Only use rating filter if it returns results
        if not rating_filtered.empty:
            filtered = rating_filtered

    filtered = filtered.dropna(subset=["restaurant_name", "location"])
    filtered = filtered.reset_index(drop=True)

    # If still empty after all filters, use full dataset
    if filtered.empty:
        filtered = df.copy()

    # Ensure rating is numeric for scoring
    filtered["rating"] = pd.to_numeric(filtered["rating"], errors="coerce").fillna(0.0)
    filtered["votes"] = pd.to_numeric(filtered["votes"], errors="coerce").fillna(0)
    
    filtered = filtered.assign(score=filtered.apply(lambda row: compute_score(row, prefs), axis=1))
    filtered = filtered.sort_values(by=["score", "rating", "votes"], ascending=[False, False, False])
    return filtered.head(top_n)


def build_recommendation_payload(filtered: pd.DataFrame) -> list[dict[str, Any]]:
    payload = []
    for _, row in filtered.iterrows():
        payload.append(
            {
                "restaurant_name": normalize_text(row["restaurant_name"]),
                "location": normalize_text(row["location"]),
                "primary_cuisine": normalize_text(row["primary_cuisine"]),
                "cuisine_tags": row["cuisine_tags"],
                "budget_label": normalize_text(row["budget_label"]),
                "rating": float(row["rating"] or 0.0),
                "votes": int(row["votes"] or 0),
                "address": normalize_text(row["address"]),
                "score": float(row["score"] or 0.0),
            }
        )
    return payload


def recommend(
    dataset_path: Path | str = "data/processed/clean_zomato_restaurants.csv",
    location: str | None = None,
    budget: str | None = None,
    cuisine: str | None = None,
    minimum_rating: float = 0.0,
    additional_preferences: list[str] | None = None,
    top_n: int = 10,
) -> list[dict[str, Any]]:
    df = load_clean_data(dataset_path)
    prefs = UserPreferences(
        location=location,
        budget=budget,
        cuisine=cuisine,
        minimum_rating=minimum_rating,
        additional_preferences=additional_preferences,
    )
    filtered = filter_restaurants(df, prefs, top_n=top_n)
    return build_recommendation_payload(filtered)
