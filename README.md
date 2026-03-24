# UI Actions API

FastAPI service that turns natural-language UI edit requests into structured `applyStyle` actions using a local [Ollama](https://ollama.com/) model (default: **Gemma 3 270M**).

## Prerequisites

- **Python** 3.10+
- **Ollama** installed and running ([download](https://ollama.com/download))
- A Gemma model pulled locally, for example:

```bash
ollama pull gemma3:270m
```

The default model is set in `model.py` as `DEFAULT_MODEL` (`gemma3:270m`). Change it to match a tag from `ollama list` if you use another model.

## Setup

Clone the repository and install dependencies:

```bash
git clone <your-repo-url>
cd <repo-directory>
python -m pip install -r requirements.txt
```

Using a virtual environment is recommended:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

With auto-reload during development:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Ollama’s HTTP API should be reachable at `http://localhost:11434` (default).

## Example request

**curl** (macOS, Linux, Git Bash on Windows):

```bash
curl -s -X POST "http://localhost:8000/generate-ui-actions" \
  -H "Content-Type: application/json" \
  -d '{"request": "hide sidebar and make background black"}'
```

**PowerShell** (Windows):

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/generate-ui-actions" `
  -Method Post -ContentType "application/json" `
  -Body '{"request": "hide sidebar and make background black"}'
```

## Configuration

| What | Where |
|------|--------|
| Ollama URL | `http://localhost:11434` — edit `OLLAMA_GENERATE_URL` in `model.py` if Ollama runs elsewhere |
| Model name | `DEFAULT_MODEL` in `model.py` |

## License

Add your license here if applicable.
