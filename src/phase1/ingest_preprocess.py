from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import pandas as pd
from datasets import load_dataset


COST_BUCKETS = [
    (0, 300, "low"),
    (301, 700, "medium"),
    (701, math.inf, "high"),
]

LOCATION_NORMALIZATION = {
    "delhi ncr": "Delhi",
    "ncr": "Delhi",
    "new delhi": "Delhi",
    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",
    "mumbai": "Mumbai",
    "bombay": "Mumbai",
    "hyderabad": "Hyderabad",
    "gurgaon": "Gurgaon",
    "gurugram": "Gurgaon",
    "noida": "Noida",
}

CUISINE_NORMALIZATION = {
    "north indian": "North Indian",
    "south indian": "South Indian",
    "chinese": "Chinese",
    "italian": "Italian",
    "continental": "Continental",
    "fast food": "Fast Food",
    "american": "American",
    "mexican": "Mexican",
    "japanese": "Japanese",
    "thai": "Thai",
    "seafood": "Seafood",
    "desserts": "Desserts",
}


def normalize_text(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_location(value: object) -> str | None:
    text = normalize_text(value)
    if not text:
        return None
    key = text.lower()
    return LOCATION_NORMALIZATION.get(key, text.title())


def normalize_cuisines(value: object) -> list[str]:
    text = normalize_text(value)
    if not text:
        return []

    if isinstance(value, list):
        cuisines = [normalize_text(part) for part in value]
    else:
        cuisines = [normalize_text(part) for part in re.split(r",|\|" , text) if normalize_text(part)]

    normalized = []
    for cuisine in cuisines:
        if not cuisine:
            continue
        lower = cuisine.lower()
        normalized.append(CUISINE_NORMALIZATION.get(lower, cuisine.title()))

    return sorted(set(normalized), key=normalized.index)


def parse_cost(value: object) -> float | None:
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    digits = re.findall(r"\d+", text)
    if digits:
        return float(digits[0])

    return None


def map_budget(cost_value: float | None) -> str | None:
    if cost_value is None or math.isnan(cost_value):
        return None
    for minimum, maximum, label in COST_BUCKETS:
        if minimum <= cost_value <= maximum:
            return label
    return None


def find_first_available_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None


def build_dataset_frame(raw_frame: pd.DataFrame) -> pd.DataFrame:
    source_columns = {
        "restaurant_name": ["restaurant_name", "name", "restaurant_name_str"],
        "location": ["location", "city", "locality", "area", "city_name"],
        "cuisines": ["cuisines", "cuisine", "cuisine_list", "categories"],
        "average_cost_for_two": ["average_cost_for_two", "cost", "price_range", "average_cost_for_two_people"],
        "rating": ["aggregate_rating", "rating", "rating_value", "avg_rating"],
        "votes": ["votes", "review_count", "num_reviews", "reviews"],
        "address": ["address", "restaurant_url", "locality_verbose", "res_address", "location_address"],
    }

    columns = {}
    for key, candidates in source_columns.items():
        column_name = find_first_available_column(raw_frame, candidates)
        columns[key] = column_name

    selected_frame = pd.DataFrame()
    selected_frame["restaurant_name"] = raw_frame[columns["restaurant_name"]] if columns["restaurant_name"] else None
    selected_frame["location"] = raw_frame[columns["location"]] if columns["location"] else None
    selected_frame["cuisine_raw"] = raw_frame[columns["cuisines"]] if columns["cuisines"] else None
    selected_frame["cost_raw"] = raw_frame[columns["average_cost_for_two"]] if columns["average_cost_for_two"] else None
    selected_frame["rating_raw"] = raw_frame[columns["rating"]] if columns["rating"] else None
    selected_frame["votes_raw"] = raw_frame[columns["votes"]] if columns["votes"] else None
    selected_frame["address"] = raw_frame[columns["address"]] if columns["address"] else None

    selected_frame["restaurant_name"] = selected_frame["restaurant_name"].apply(normalize_text)
    selected_frame["location"] = selected_frame["location"].apply(normalize_location)
    selected_frame["cuisine_tags"] = selected_frame["cuisine_raw"].apply(normalize_cuisines)
    selected_frame["primary_cuisine"] = selected_frame["cuisine_tags"].apply(lambda tags: tags[0] if tags else None)
    selected_frame["cost"] = selected_frame["cost_raw"].apply(parse_cost)
    selected_frame["budget_label"] = selected_frame["cost"].apply(map_budget)
    selected_frame["rating"] = pd.to_numeric(selected_frame["rating_raw"], errors="coerce")
    selected_frame["votes"] = pd.to_numeric(selected_frame["votes_raw"], errors="coerce").fillna(0).astype(int)
    selected_frame["address"] = selected_frame["address"].apply(normalize_text)

    selected_frame["affordability"] = selected_frame["budget_label"].copy()
    selected_frame["affordability"] = selected_frame["affordability"].fillna("unknown")
    selected_frame["primary_cuisine"] = selected_frame["primary_cuisine"].fillna("Other")

    cleaned = selected_frame[
        [
            "restaurant_name",
            "location",
            "primary_cuisine",
            "cuisine_tags",
            "cost",
            "budget_label",
            "rating",
            "votes",
            "address",
            "affordability",
        ]
    ].copy()

    cleaned = cleaned.dropna(subset=["restaurant_name", "location"])
    cleaned = cleaned.reset_index(drop=True)
    return cleaned


def save_clean_data(clean_frame: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "clean_zomato_restaurants.csv"
    parquet_path = output_dir / "clean_zomato_restaurants.parquet"

    clean_frame.to_csv(csv_path, index=False)
    clean_frame.to_parquet(parquet_path, index=False)

    print(f"Saved cleaned data to: {csv_path}")
    print(f"Saved cleaned data to: {parquet_path}")


def load_raw_dataset(dataset_id: str) -> pd.DataFrame:
    dataset = load_dataset(dataset_id)
    if isinstance(dataset, dict) and "train" in dataset:
        frame = pd.DataFrame(dataset["train"])
    elif hasattr(dataset, "to_pandas"):
        frame = dataset.to_pandas()
    else:
        frame = pd.concat([pd.DataFrame(split) for split in dataset.values()], ignore_index=True)

    print(f"Loaded raw dataset with {len(frame):,} records and {len(frame.columns)} columns")
    return frame


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load and preprocess the Zomato restaurant recommendation dataset."
    )
    parser.add_argument(
        "--dataset-id",
        default="ManikaSaini/zomato-restaurant-recommendation",
        help="Hugging Face dataset identifier",
    )
    parser.add_argument(
        "--output-dir",
        default="src/phase1/data/processed",
        help="Directory for cleaned dataset output files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    output_dir = Path(args.output_dir)

    raw_frame = load_raw_dataset(args.dataset_id)
    cleaned_frame = build_dataset_frame(raw_frame)
    save_clean_data(cleaned_frame, output_dir)

    print("Phase 1 complete: Data ingestion and preprocessing finished.")


if __name__ == "__main__":
    main()
