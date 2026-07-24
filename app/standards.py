"""
Translates a raw predicted strength value into a plain-language structural
recommendation, per the three-tier system defined in the project brief
(High Strength / Moderate Strength / Low Strength).

IMPORTANT: The thresholds below are placeholders for you to replace with the
exact clause values from the specific standard your brief references (NIS 87,
BS 6073, or whichever you settled on). Don't ship these numbers as-is —
confirm them against your actual source document before this goes in front of
anyone evaluating the project.
"""

# Placeholder thresholds in N/mm2 — replace with your verified standard values
LOAD_BEARING_MIN = 3.45
NON_LOAD_BEARING_MIN = 2.5


def recommend(predicted_strength: float) -> str:
    if predicted_strength >= LOAD_BEARING_MIN:
        return (
            "The predicted strength is excellent for load-bearing walls. "
            "Blocks can be safely used for structural applications. "
            "Ensure standard quality control during production."
        )
    elif predicted_strength >= NON_LOAD_BEARING_MIN:
        return (
            "The predicted strength is acceptable, but monitor production quality. "
            "Adjust mix ratio, water-cement ratio, or curing if needed for consistency."
        )
    else:
        return (
            "The predicted strength is below recommended standards. "
            "Consider increasing cement content, optimizing water-cement ratio, "
            "or improving curing methods to enhance block performance."
        )