"""
Produces per-feature SHAP contributions for a single prediction, so the
frontend can show "why" the model predicted a given strength.
"""

import shap
import time

from app.model_service import get_pipeline, input_to_dataframe
from app.schemas import PredictionInput, FeatureContribution

_explainer = None


def _get_explainer():
    global _explainer
    if _explainer is None:
        start = time.time()
        print("[shap_service] Initializing SHAP explainer", flush=True)
        pipeline = get_pipeline()
        tree_model = pipeline.named_steps["model"]
        _explainer = shap.TreeExplainer(tree_model)
        duration = time.time() - start
        print(f"[shap_service] SHAP explainer initialized in {duration:.3f}s", flush=True)
    return _explainer


def explain(data: PredictionInput) -> list[FeatureContribution]:
    pipeline = get_pipeline()
    df = input_to_dataframe(data)
    start = time.time()
    print("[shap_service] Transforming input for SHAP", flush=True)
    transformed = pipeline.named_steps["preprocess"].transform(df)

    explainer = _get_explainer()
    print("[shap_service] Computing SHAP values", flush=True)
    shap_values = explainer.shap_values(transformed)[0]
    duration = time.time() - start
    print(f"[shap_service] SHAP explanation completed in {duration:.3f}s", flush=True)

    feature_names = df.columns.tolist()
    contributions = [
        FeatureContribution(feature=name, contribution=float(value))
        for name, value in zip(feature_names, shap_values)
    ]
    # Largest absolute contribution first — most informative for the frontend chart
    contributions.sort(key=lambda c: abs(c.contribution), reverse=True)
    return contributions
