"""
Scoring: converts extracted movement data into category-wise skill scores
(0-100) and specific, actionable feedback text.
"""

CATEGORIES = ["control", "technique", "balance", "accuracy"]


def score_movement(movement_data: dict, drill_type: str) -> dict:
    foot_ball_distance = movement_data["foot_ball_distance_cm"]
    balance_stability = movement_data["balance_stability"]
    follow_through = movement_data["follow_through_consistency"]
    angle_deviation = movement_data["contact_angle_deviation_deg"]

    # Lower foot-ball distance and angle deviation = better; higher stability/follow-through = better
    control_score = _clamp(100 - foot_ball_distance * 4)
    technique_score = _clamp(100 - angle_deviation * 2)
    balance_score = _clamp(balance_stability * 100)
    accuracy_score = _clamp((follow_through * 60) + (100 - angle_deviation * 1.5) * 0.4)

    scores = {
        "control": round(control_score, 1),
        "technique": round(technique_score, 1),
        "balance": round(balance_score, 1),
        "accuracy": round(accuracy_score, 1),
    }

    feedback = _generate_feedback(scores, foot_ball_distance, angle_deviation, drill_type)

    return {"scores": scores, "feedback": feedback}


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def _generate_feedback(scores: dict, foot_ball_distance: float, angle_deviation: float, drill_type: str) -> list:
    feedback = []

    if scores["control"] < 60:
        feedback.append(
            f"Your plant foot is roughly {foot_ball_distance:.1f}cm from the ball at contact — "
            f"aim to get it closer for cleaner {drill_type} control."
        )
    if scores["technique"] < 60:
        feedback.append(
            f"Contact angle deviates by about {angle_deviation:.1f}° from ideal form — "
            f"focus on a consistent strike angle."
        )
    if scores["balance"] < 60:
        feedback.append("Your balance dips during the movement — core stability drills will help here.")
    if scores["accuracy"] < 60:
        feedback.append("Follow-through is inconsistent — practice completing the motion fully each time.")

    if not feedback:
        feedback.append(f"Strong {drill_type} technique overall — keep reinforcing with consistent reps.")

    return feedback


def weakest_category(scores: dict) -> str:
    return min(scores, key=scores.get)
