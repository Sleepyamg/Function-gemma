# UI Actions API

FastAPI service that turns natural-language UI edit requests into structured `applyStyle` actions via a local Ollama model (Gemma).

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with a Gemma model pulled, for example:

```bash
ollama pull gemma3:270m
```

The default model name in `model.py` is `gemma3:270m` (Gemma 3 270M, small on disk). To use another tag, set `DEFAULT_MODEL` in `model.py` to match `ollama list`.

## Install

```bash
cd d:\freelance\ai-api
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Development with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`

## Example

```bash
curl -X POST "http://localhost:8000/generate-ui-actions" ^
  -H "Content-Type: application/json" ^
  -d "{\"request\": \"hide sidebar and make background black\"}"
```

Ollama must be listening at `http://localhost:11434` (default).
