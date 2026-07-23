# Enterprise RAG Knowledge Platform

A practical FastAPI service for indexed enterprise search, grounded answers, and source-backed retrieval across internal knowledge content.

## What it does

- Ingests knowledge records with titles and body text
- Breaks content into searchable snippets
- Returns ranked matches with citations
- Exposes a simple streaming endpoint for knowledge events
- Ships with smoke tests and packaging metadata

## API

- `GET /health` - service readiness
- `POST /knowledge` - ingest a knowledge item
- `GET /knowledge/{item_id}` - inspect a stored item
- `POST /search` - retrieve ranked knowledge snippets for a question
- `WS /ws/knowledge` - stream ingestion events

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
uvicorn src.main:app --reload
```
