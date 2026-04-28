# Data Ingestion and Preprocessing

This folder contains the Phase 1 implementation for the Zomato restaurant recommendation project.

## Files
- `ingest_preprocess.py`: loads the Hugging Face dataset, normalizes key restaurant fields, and saves cleaned output.

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the preprocessing script:
   ```bash
   python src/phase1/ingest_preprocess.py --output-dir src/phase1/data/processed
   ```

## Output
- `src/phase1/data/processed/clean_zomato_restaurants.csv`
- `src/phase1/data/processed/clean_zomato_restaurants.parquet`
