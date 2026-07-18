"""
FastAPI application entry point.

Run locally with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000 for the form, or http://127.0.0.1:8000/docs
for the auto-generated interactive API docs.
"""

from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import model_service, shap_service, standards
from app.schemas import PredictionInput, PredictionOutput, ExplanationOutput

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Sandcrete Compressive Strength Predictor")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    try:
        strength = model_service.predict(data)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return PredictionOutput(
        predicted_strength=round(strength, 3),
        standards_recommendation=standards.recommend(strength),
    )


@app.post("/explain", response_model=ExplanationOutput)
def explain(data: PredictionInput):
    try:
        strength = model_service.predict(data)
        contributions = shap_service.explain(data)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return ExplanationOutput(
        predicted_strength=round(strength, 3),
        contributions=contributions,
    )


@app.get("/health")
def health():
    return {"status": "ok"}
