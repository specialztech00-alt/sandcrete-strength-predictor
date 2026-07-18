"""
Translates a raw predicted strength value into a plain-language recommendation
(e.g. suitable for load-bearing walls vs non-load-bearing partitions only).

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
            f"Predicted strength {predicted_strength:.2f} N/mm2 meets the load-bearing "
            f"threshold (>= {LOAD_BEARING_MIN} N/mm2, placeholder value — verify against your standard)."
        )
    elif predicted_strength >= NON_LOAD_BEARING_MIN:
        return (
            f"Predicted strength {predicted_strength:.2f} N/mm2 is suitable for non-load-bearing "
            f"applications only (>= {NON_LOAD_BEARING_MIN} N/mm2, placeholder value — verify against your standard)."
        )
    else:
        return (
            f"Predicted strength {predicted_strength:.2f} N/mm2 falls below both placeholder "
            "thresholds — mix design likely needs adjustment."
        )
