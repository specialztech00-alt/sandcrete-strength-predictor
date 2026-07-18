import joblib

p = joblib.load('model/sandcrete_pipeline.pkl')
print('PIPELINE_TYPE', type(p).__module__, type(p).__name__)
print('STEPS', list(p.named_steps.keys()))
for name, step in p.named_steps.items():
    print('STEP', name, type(step).__module__, type(step).__name__)
    print('  CLASS_MODULE', step.__class__.__module__)
