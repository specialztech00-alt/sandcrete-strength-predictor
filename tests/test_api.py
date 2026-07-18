"""
Tests the API layer without requiring the real trained model — a fake
pipeline is substituted in via monkeypatch so these tests run even before
you've copied sandcrete_pipeline.pkl into the model/ folder.

Run with:
    pytest
"""

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app import model_service

client = TestClient(app)


class FakeModel:
    """Stands in for the real GradientBoostingRegressor etc."""
    def predict(self, X):
        return [5.0] * len(X)


class FakePreprocessor:
    def transform(self, X):
        return X.values


class FakePipeline:
    def __init__(self):
        self.named_steps = {"preprocess": FakePreprocessor(), "model": FakeModel()}

    def predict(self, X):
        return self.named_steps["model"].predict(X)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_with_fake_model(monkeypatch):
    monkeypatch.setattr(model_service, "_pipeline", FakePipeline())
    monkeypatch.setattr(model_service, "_load_pipeline", lambda: model_service._pipeline)

    payload = {
        "curing_technique": "air",
        "cement_brand": "Dangote",
        "mix_ratio": "1:5",
        "curing_age": 28,
        "water_cement_ratio": 0.5,
    }
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["predicted_strength"] == 5.0
    assert "standards_recommendation" in body


def test_predict_missing_model_returns_503(monkeypatch):
    monkeypatch.setattr(model_service, "_pipeline", None)

    def raise_not_found():
        raise FileNotFoundError("model missing")

    monkeypatch.setattr(model_service, "_load_pipeline", raise_not_found)

    payload = {
        "curing_technique": "air",
        "cement_brand": "Dangote",
        "mix_ratio": "1:5",
        "curing_age": 28,
        "water_cement_ratio": 0.5,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 503


def test_invalid_input_rejected():
    payload = {
        "curing_technique": "air",
        "cement_brand": "Dangote",
        "mix_ratio": "1:5",
        "curing_age": -5,  # invalid: must be > 0
        "water_cement_ratio": 0.5,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
