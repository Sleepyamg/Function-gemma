from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from model import DEFAULT_MODEL, generate_raw_response
from parser import normalize_actions_payload, parse_ui_actions_response

app = FastAPI(title="UI Actions Generator", version="1.0.0")


class GenerateUIActionsRequest(BaseModel):
    request: str = Field(..., min_length=1)


class ApplyStyleParams(BaseModel):
    selector: str
    styles: dict[str, Any]


class UIAction(BaseModel):
    function: str = "applyStyle"
    params: ApplyStyleParams


class GenerateUIActionsResponse(BaseModel):
    actions: list[UIAction]


@app.post("/generate-ui-actions", response_model=GenerateUIActionsResponse)
def generate_ui_actions(body: GenerateUIActionsRequest) -> GenerateUIActionsResponse:
    try:
        raw = generate_raw_response(body.request, model=DEFAULT_MODEL)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {e}") from e

    parsed = parse_ui_actions_response(raw)
    normalized = normalize_actions_payload(parsed)
    return GenerateUIActionsResponse.model_validate(normalized)
