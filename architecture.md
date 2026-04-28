# AI-Powered Restaurant Recommendation System Architecture

## Overview
This architecture describes a phase-wise design for building an AI-powered restaurant recommendation service using the Zomato dataset. The system combines structured data ingestion, preference filtering, LLM reasoning, and user-friendly output presentation.

## Phase 1: Data Ingestion & Preprocessing

### Objectives
- Acquire the Zomato dataset from Hugging Face
- Extract and normalize restaurant fields
- Store cleaned data for consumption

### Components
- Data acquisition module
- ETL preprocessing pipeline
- Data store (local file or relational database)

### Tasks
1. Download the dataset from `https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation`
2. Inspect dataset schema and sample records
3. Extract relevant fields:
   - restaurant_name
   - location
   - cuisine
   - average_cost_for_two / cost
   - aggregate_rating / rating
   - votes / review_count
   - restaurant_url / address / locality
   - cuisine_list / categories
4. Normalize and clean values:
   - standardize locations (e.g. Delhi, Bangalore, Mumbai)
   - map cost values to categories: `low`, `medium`, `high`
   - clean cuisine tags and unify similar cuisines
   - convert ratings to numeric values and validate ranges
5. Enrich with derived attributes:
   - affordability label
   - cuisine primary category
   - popularity score (optional)
6. Persist cleaned data into a structured store:
   - CSV/JSON/Parquet file
   - SQLite or PostgreSQL database
   - Optional vector store if later personalization or semantic search is added

### Output
- A cleaned dataset ready for querying
- Data access layer for later phases

## Phase 2: Preferences & Filtering Layer

### Objectives
- Capture user preferences
- Apply deterministic filtering to generate a candidate set

### Components
- Preference model / schema
- Filter engine
- Matching and ranking heuristics

### Tasks
1. Design the user preference schema:
   - location
   - budget (`low`, `medium`, `high`)
   - cuisine
   - minimum_rating
   - additional preferences (family-friendly, quick service, outdoor seating, vegetarian options)
2. Create input validation and normalization:
   - normalize location names
   - validate budget categories
   - map user text to supported cuisines
3. Build the filter engine:
   - apply location constraints
   - apply budget constraint using cost category
   - filter by cuisine match or cuisine subset
   - enforce minimum rating threshold
4. Add heuristic scoring for candidate selection:
   - exact match boost for location and cuisine
   - rating weight
   - closeness of cost category to user budget
   - optional bonus for family-friendly / quick service tags
5. Generate candidate shortlist:
   - top N restaurants after filtering and heuristic scoring
   - optionally include fallback logic if shortlist is too small

### Output
- A ranked shortlist of structured restaurant candidates
- JSON-ready candidate data for prompt construction

## Phase 3: LLM Integration & Prompt Design

### Objectives
- Convert structured candidates into LLM-ready input
- Build prompt templates for ranking, explanation, and summary
- Use Groq LLM for ranking and human-friendly explanation generation

### Components
- Prompt builder
- Groq LLM client / API connector
- Output parser
- `.env`-backed configuration for the Groq API key

### Tasks
1. Define the integration contract:
   - structured context from candidate list
   - user preference summary
   - instruction for ranking and explanation
2. Store the Groq API key in a `.env` file and load it securely in the integration layer
2. Create prompt templates with clear roles:
   - system prompt describing assistant behavior
   - user prompt summarizing preferences and asking for recommendations
3. Include structured restaurant context:
   - name, cuisine, rating, cost category, location, key features
   - short notes or highlights from the data store
4. Instruct the LLM to:
   - rank the candidate restaurants by relevance
   - provide short reasoning for each recommended restaurant
   - generate a friendly summary and why the result fits the user
5. Implement LLM call flow:
   - send prompt and candidate data to chosen model API
   - handle rate limiting, retries, and error cases
6. Parse the LLM response:
   - extract ranked restaurant list
   - extract written explanations
   - validate consistency with the structured candidates

### Output
- LLM-generated ranked recommendations
- Explanation text for each restaurant
- Summary statement for final output

## Phase 4: Recommendation Engine & Response Formatting

### Objectives
- Merge filtered results with LLM output
- Generate the final presentation-ready recommendation payload

### Components
- Recommendation assembler
- Formatter / response builder
- Validation logic

### Tasks
1. Combine filter results and LLM response:
   - ensure recommended items match the candidate shortlist
   - preserve structured attributes for display
2. Build final response format:
   - restaurant name
   - cuisine
   - rating
   - estimated cost category
   - short AI-generated explanation
   - optional tags/notes
3. Create user-facing summary:
   - highlight top match
   - describe why recommendations fit preferences
   - mention any special constraints or tradeoffs
4. Provide fallback messaging when no match found:
   - suggest relaxing budget or rating
   - offer alternate cuisine/location options
5. Optional analytics capture:
   - track which candidate caused ranking decisions
   - log LLM outputs for review and prompt tuning

### Output
- Final recommendation payload for UI or API consumers
- Clean, consistent format for display

## Phase 5: UI/UX, Deployment, and Iteration

### Objectives
- Expose the recommendation service via a REST API and frontend website
- Deploy and iterate with observability and user feedback
- Provide a user-friendly web interface for inputting preferences and viewing recommendations

### Components
- Frontend Website (React/Vue.js or Flask-based HTML/CSS)
- REST API backend (Flask/FastAPI)
- Deployment pipeline
- Logging and monitoring

### Tasks
1. Build the REST API backend:
   - `/api/recommend` — POST endpoint for preference submission and recommendation retrieval
   - `/api/health` — GET endpoint for service status
   - `/api/feedback` — POST endpoint for user rating of recommendations (optional)
   - CORS configuration for frontend integration
   - Request validation and error handling

2. Implement the frontend website:
   - Responsive web UI (HTML, CSS, JavaScript)
   - Preference input form with dropdowns/text fields for location, budget, cuisine, rating
   - Restaurant recommendation cards displaying name, cuisine, rating, budget, and AI explanation
   - Summary section highlighting top match and why it fits
   - Filter adjustment UI for re-running recommendations
   - Loading states and error messaging
   - Mobile-friendly responsive design

3. Frontend Features:
   - Dynamic form validation
   - Real-time filtering as user adjusts preferences
   - Restaurant detail modal/popup for more information
   - "Try Again" button to modify preferences and re-submit
   - Share recommendation feature (optional)

4. Configure deployment:
   - Local development environment with hot reload
   - containerized deployment with Docker (optional)
   - cloud deployment (AWS, GCP, Heroku) if desired
   - environment-based configuration (dev, staging, production)

5. Add logging and metrics:
   - API request/response logging
   - LLM latency and error metrics
   - data pipeline health checks
   - frontend error tracking and user analytics

6. Iterate based on user feedback:
   - refine prompt templates
   - improve filter heuristics
   - expand dataset fields and personalization
   - add support for new preference dimensions
   - optimize UI/UX based on user interaction data

### Output
- Deployed website at accessible URL
- REST API endpoints for backend services
- User-friendly recommendation interface
- Ongoing improvement pipeline


## Architecture Layers Summary
- Data Layer: ingestion, normalization, storage
- Business Layer: preference modeling, filtering, ranking heuristics
- AI Layer: prompt construction, LLM ranking, explanation generation
- Presentation Layer: formatted output and UI integration

## Suggested File Structure
- `data/` — dataset ingestion and preprocessing scripts
- `models/` — preference schema and candidate models
- `llm/` — prompt templates and LLM integration code
- `service/` — recommendation engine and API endpoints
- `ui/` — frontend or CLI interface
- `docs/architecture.md` — this design document
