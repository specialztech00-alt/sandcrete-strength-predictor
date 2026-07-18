"""
Loads the trained pipeline exported from the Colab notebook and runs
predictions on it. This is the ONLY place that touches the .pkl file —
everything else in the app talks to the functions below, never to the
pipeline object directly.
"""

from pathlib import Path
import joblib
import pandas as pd
import time

from app.schemas import PredictionInput

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "sandcrete_pipeline.pkl"

_pipeline = None  # lazy-loaded so the app can still start (e.g. for tests) without the file present


def _load_pipeline():
    global _pipeline
    if _pipeline is None:
        start = time.time()
        print(f"[model_service] Loading pipeline from {MODEL_PATH}", flush=True)
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"No trained model found at {MODEL_PATH}. "
                "Copy sandcrete_pipeline.pkl from the Colab notebook's export/ folder "
                "into this project's model/ directory."
            )
        _pipeline = joblib.load(MODEL_PATH)
        duration = time.time() - start
        print(f"[model_service] Loaded pipeline in {duration:.3f}s", flush=True)
    return _pipeline


def input_to_dataframe(data: PredictionInput) -> pd.DataFrame:
    """
    Converts the API's request schema into the exact column shape the
    pipeline was trained on. Must match feature_cols in the training
    notebook: ['CuringTechnique', 'CementBrand', 'MixRatioValue', 'CuringAge', 'WaterCementRatio']
    """
    mix_ratio_value = float(data.mix_ratio.split(":")[1])

    return pd.DataFrame([{
        "CuringTechnique": data.curing_technique,
        "CementBrand": data.cement_brand,
        "MixRatioValue": mix_ratio_value,
        "CuringAge": data.curing_age,
        "WaterCementRatio": data.water_cement_ratio,
    }])


def predict(data: PredictionInput) -> float:
    pipeline = _load_pipeline()
    df = input_to_dataframe(data)
    start = time.time()
    print("[model_service] Running prediction", flush=True)
    prediction = pipeline.predict(df)[0]
    duration = time.time() - start
    print(f"[model_service] Prediction completed in {duration:.3f}s", flush=True)
    return float(prediction)


def get_pipeline():
    """Exposed for shap_service.py, which needs the fitted model + preprocessor separately."""
    return _load_pipeline()
