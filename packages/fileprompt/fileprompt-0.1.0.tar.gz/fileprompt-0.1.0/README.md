# Repo Prompt Prototype

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000

## About

This is a fast‑iterating prototype that lets users browse a local project, select files, add instructions and copy a prompt formatted for LLM consumption.

See `app/` for backend implementation and `templates/index.html` for the minimal HTMX/Alpine UI.