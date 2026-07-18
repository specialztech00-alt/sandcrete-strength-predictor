"""
Request and response models for the API.

These mirror the exact feature columns used to train the model in the Colab
notebook: CuringTechnique, CementBrand, MixRatio, CuringAge, WaterCementRatio.
If you change the training feature set, update this file and model_service.py
together — they must always agree on column names and order.
"""

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    curing_technique: str = Field(..., json_schema_extra={"example": "air"}, description="e.g. air, sprinkling, submerged")
    cement_brand: str = Field(..., json_schema_extra={"example": "Dangote"}, description="e.g. Purechem, BUA, Lafarge, Dangote")
    mix_ratio: str = Field(..., json_schema_extra={"example": "1:5"}, description="Cement:sand ratio as a string, e.g. '1:5'")
    curing_age: float = Field(..., gt=0, json_schema_extra={"example": 28}, description="Curing age in days")
    water_cement_ratio: float = Field(..., gt=0, lt=2, json_schema_extra={"example": 0.5})


class PredictionOutput(BaseModel):
    predicted_strength: float
    unit: str = "N/mm2"
    standards_recommendation: str


class FeatureContribution(BaseModel):
    feature: str
    contribution: float


class ExplanationOutput(BaseModel):
    predicted_strength: float
    contributions: list[FeatureContribution]
