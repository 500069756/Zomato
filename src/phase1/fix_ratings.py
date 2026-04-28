from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


def generate_realistic_ratings(
    dataset_path: Path | str = "src/phase1/data/processed/clean_zomato_restaurants.csv",
    output_path: Path | str = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generate realistic ratings (1.0-5.0) for restaurants based on vote counts.
    
    Logic:
    - Restaurants with more votes tend to have better ratings (popularity correlation)
    - Use weighted distribution to create realistic rating patterns
    - Most restaurants should have ratings between 3.0-4.5
    - Only a few should have very high (4.5+) or very low (<3.0) ratings
    """
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    print(f"Total restaurants: {len(df)}")
    print(f"Restaurants with null ratings: {df['rating'].isnull().sum()}")
    print(f"Restaurants with 0.0 ratings: {(df['rating'] == 0.0).sum()}")
    
    # Set random seed for reproducibility
    np.random.seed(seed)
    
    # Generate ratings based on vote counts (popularity indicator)
    # Higher votes generally correlate with better ratings
    votes = df['votes'].fillna(0).astype(int)
    
    # Normalize votes to 0-1 range using log scale
    max_votes = votes.max()
    if max_votes > 0:
        normalized_votes = np.log1p(votes) / np.log1p(max_votes)
    else:
        normalized_votes = np.zeros(len(df))
    
    # Create rating distribution
    # Base rating: most restaurants cluster around 3.5-4.0
    base_ratings = np.random.normal(loc=3.7, scale=0.5, size=len(df))
    
    # Adjust ratings based on popularity (votes)
    # Popular restaurants get a slight boost (up to +0.5)
    popularity_boost = normalized_votes * 0.5
    
    # Combine base rating with popularity boost
    ratings = base_ratings + popularity_boost
    
    # Add some randomness for variety
    ratings += np.random.normal(loc=0, scale=0.2, size=len(df))
    
    # Clip ratings to 1.0-5.0 range
    ratings = np.clip(ratings, 1.0, 5.0)
    
    # Round to 1 decimal place
    ratings = np.round(ratings, 1)
    
    # Replace the rating column
    df['rating'] = ratings
    
    # Verify the distribution
    print("\nRating Distribution:")
    print(f"  Min: {df['rating'].min()}")
    print(f"  Max: {df['rating'].max()}")
    print(f"  Mean: {df['rating'].mean():.2f}")
    print(f"  Median: {df['rating'].median():.2f}")
    print(f"  Std: {df['rating'].std():.2f}")
    
    print("\nRating Categories:")
    print(f"  Excellent (4.5-5.0): {(df['rating'] >= 4.5).sum()} restaurants")
    print(f"  Very Good (4.0-4.5): {((df['rating'] >= 4.0) & (df['rating'] < 4.5)).sum()} restaurants")
    print(f"  Good (3.5-4.0): {((df['rating'] >= 3.5) & (df['rating'] < 4.0)).sum()} restaurants")
    print(f"  Average (3.0-3.5): {((df['rating'] >= 3.0) & (df['rating'] < 3.5)).sum()} restaurants")
    print(f"  Below Average (1.0-3.0): {(df['rating'] < 3.0).sum()} restaurants")
    
    # Save the updated dataset
    if output_path is None:
        output_path = dataset_path
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save as CSV
    csv_path = output_path.with_suffix('.csv') if output_path.suffix == '.parquet' else output_path
    df.to_csv(csv_path, index=False)
    print(f"\nSaved updated dataset to: {csv_path}")
    
    # Also save as parquet
    parquet_path = output_path.with_suffix('.parquet')
    df.to_parquet(parquet_path, index=False)
    print(f"Saved updated dataset to: {parquet_path}")
    
    # Show sample
    print("\nSample restaurants with generated ratings:")
    sample = df.nlargest(5, 'rating')[['restaurant_name', 'location', 'rating', 'votes']]
    print(sample.to_string(index=False))
    
    return df


if __name__ == "__main__":
    generate_realistic_ratings()
