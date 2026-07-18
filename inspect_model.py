"""Inspect the pipeline structure."""
import sys
import joblib
import pandas as pd

p = joblib.load('model/sandcrete_pipeline.pkl')
print("=== PIPELINE TYPE ===")
print(type(p))

print("\n=== NAMED STEPS ===")
for name, step in p.named_steps.items():
    print(f"  {name}: {type(step).__name__}")

# Inspect preprocessor
for step_name in list(p.named_steps.keys()):
    step = p.named_steps[step_name]
    if hasattr(step, 'transformers_'):
        print(f"\n=== PREPROCESSOR ({step_name}) ===")
        for t_name, t_obj, t_cols in step.transformers_:
            print(f"  Transformer: {t_name} ({type(t_obj).__name__}) -> columns: {t_cols}")
            if hasattr(t_obj, 'categories_'):
                for i, cat in enumerate(t_obj.categories_):
                    print(f"    categories_[{i}]: {list(cat)}")
        if hasattr(step, 'remainder'):
            print(f"  Remainder: {step.remainder}")

# Model info
model = list(p.named_steps.values())[-1]
print(f"\n=== MODEL ===")
print(f"Type: {type(model).__name__}")
if hasattr(model, 'n_features_in_'):
    print(f"N features in: {model.n_features_in_}")

# Test predictions
print("\n=== TEST PREDICTIONS ===")
tests = [
    ("lowercase", {"CuringTechnique": "submerged", "CementBrand": "Dangote", "MixRatioValue": 6.0, "CuringAge": 28.0, "WaterCementRatio": 0.55}),
    ("air", {"CuringTechnique": "air", "CementBrand": "Dangote", "MixRatioValue": 6.0, "CuringAge": 28.0, "WaterCementRatio": 0.55}),
    ("Open Air", {"CuringTechnique": "Open Air", "CementBrand": "Dangote", "MixRatioValue": 6.0, "CuringAge": 28.0, "WaterCementRatio": 0.55}),
    ("Title Submerged", {"CuringTechnique": "Submerged", "CementBrand": "Dangote", "MixRatioValue": 6.0, "CuringAge": 28.0, "WaterCementRatio": 0.55}),
    ("Full brand", {"CuringTechnique": "submerged", "CementBrand": "Dangote Cement", "MixRatioValue": 6.0, "CuringAge": 28.0, "WaterCementRatio": 0.55}),
    ("Purechem air 1:10", {"CuringTechnique": "air", "CementBrand": "Purechem", "MixRatioValue": 10.0, "CuringAge": 7.0, "WaterCementRatio": 0.65}),
]
for label, data in tests:
    try:
        df = pd.DataFrame([data])
        result = p.predict(df)
        print(f"  {label}: {result[0]:.3f}")
    except Exception as e:
        print(f"  {label}: ERROR - {e}")

sys.stdout.flush()
