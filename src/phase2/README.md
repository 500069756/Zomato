# Phase 2 Recommendation Service

This module implements Phase 2 of the architecture: user preference filtering, heuristic scoring, and candidate shortlist generation.

## Files
- `service/recommender.py`: preference schema and recommendation filter engine
- `recommend.py`: CLI wrapper to run recommendations against cleaned Phase 1 data

## Usage
1. Ensure Phase 1 has produced cleaned data in `src/phase1/data/processed/clean_zomato_restaurants.csv`
2. Run the recommendation CLI:
   ```bash
   python src/phase2/recommend.py --location Delhi --budget medium --cuisine Chinese --minimum-rating 4.0
   ```

## Behavior
- Applies location, budget, cuisine, and rating filters
- Scores candidates using rating, vote count, and preference matches
- Returns the top matching restaurants as a ranked shortlist
