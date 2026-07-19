"""
Training plan generator: turns a player's accumulated skill history into a
personalized weekly plan targeting their weakest category.
"""
from collections import defaultdict

DRILLS_BY_CATEGORY = {
    "control": [
        "Cone dribbling: 4 sets of 10 touches, both feet",
        "Wall passes: 50 reps focusing on first-touch cushioning",
    ],
    "technique": [
        "Slow-motion shooting form drill: 20 reps, focus on plant-foot placement",
        "Passing accuracy gates: 30 reps at 10m",
    ],
    "balance": [
        "Single-leg balance holds: 3 x 30 seconds each leg",
        "Agility ladder + ball control combo: 5 sets",
    ],
    "accuracy": [
        "Target shooting: 20 shots at marked corners",
        "Follow-through shadow drills (no ball): 3 sets of 10",
    ],
}


def generate_training_plan(skill_scores) -> dict:
    """
    skill_scores: list of SkillScore ORM rows (category, score)
    Returns a weekly plan dict targeting the lowest-average category.
    """
    totals = defaultdict(list)
    for s in skill_scores:
        totals[s.category].append(s.score)

    averages = {cat: sum(vals) / len(vals) for cat, vals in totals.items()}
    if not averages:
        return {"focus_area": None, "message": "No sessions yet — upload a drill video to get started."}

    weakest = min(averages, key=averages.get)

    return {
        "focus_area": weakest,
        "average_score": round(averages[weakest], 1),
        "all_averages": {k: round(v, 1) for k, v in averages.items()},
        "weekly_drills": DRILLS_BY_CATEGORY.get(weakest, []),
        "message": f"This week, focus on {weakest} — it's your lowest-scoring area (avg {averages[weakest]:.0f}/100).",
    }
