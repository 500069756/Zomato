from __future__ import annotations

import argparse
from pathlib import Path

from .service.recommender import recommend


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 2 recommendation filtering on cleaned Zomato data.")
    parser.add_argument("--dataset-path", default="src/phase1/data/processed/clean_zomato_restaurants.csv", help="Path to the cleaned dataset file.")
    parser.add_argument("--location", default=None, help="Preferred location.")
    parser.add_argument("--budget", default=None, choices=["low", "medium", "high"], help="Preferred budget category.")
    parser.add_argument("--cuisine", default=None, help="Preferred cuisine.")
    parser.add_argument("--minimum-rating", type=float, default=0.0, help="Minimum rating threshold.")
    parser.add_argument("--additional-preferences", default=None, help="Comma-separated extra preferences.")
    parser.add_argument("--top-n", type=int, default=10, help="Number of candidate restaurants to return.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    additional_preferences = (
        [item.strip() for item in args.additional_preferences.split(",") if item.strip()]
        if args.additional_preferences
        else []
    )
    recommendations = recommend(
        dataset_path=Path(args.dataset_path),
        location=args.location,
        budget=args.budget,
        cuisine=args.cuisine,
        minimum_rating=args.minimum_rating,
        additional_preferences=additional_preferences,
        top_n=args.top_n,
    )

    if not recommendations:
        print("No matching restaurants found. Try relaxing the filters.")
        return

    print("Top recommendations:")
    for index, item in enumerate(recommendations, start=1):
        print(f"\n{index}. {item['restaurant_name']}")
        print(f"   Location: {item['location']}")
        print(f"   Cuisine: {item['primary_cuisine']}")
        print(f"   Budget: {item['budget_label']}")
        print(f"   Rating: {item['rating']} ({item['votes']} votes)")
        print(f"   Score: {item['score']:.2f}")
        if item.get("address"):
            print(f"   Address: {item['address']}")


if __name__ == "__main__":
    main()
