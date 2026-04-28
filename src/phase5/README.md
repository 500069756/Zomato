# Phase 5: Frontend Website and API Backend

This folder provides a minimal Flask-based frontend and backend to test the recommendation pipeline end to end.

## Files
- `app.py`: Flask backend serving the web UI and `/api/recommend` endpoint
- `templates/index.html`: frontend web page for entering preferences
- `static/style.css`: UI styling
- `static/app.js`: client-side JavaScript for form submission and rendering results

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the backend from project root:
   ```bash
   python src/phase5/app.py
   ```
3. Open your browser at `http://127.0.0.1:8000`

## Behavior
- Submits user preferences to `/api/recommend`
- Uses Phase 2 candidate filtering
- Calls Groq LLM for explanations if API key is configured
- Uses Phase 4 formatting for final results

## Notes
- Ensure Phase 1 has produced cleaned data in `src/phase1/data/processed`
- Ensure `GROQ_API_KEY` is set in a `.env` file or environment variable
