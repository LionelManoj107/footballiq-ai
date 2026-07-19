"""
FootballIQ AI - FastAPI backend
Endpoints:
  POST /players            -> create a player
  POST /sessions            -> upload a drill video, get AI skill scores + feedback
  GET  /players/{id}/history -> a player's skill history
  GET  /players/{id}/plan    -> personalized weekly training plan
"""
import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from models import init_db, get_session, Player, DrillSession, SkillScore
from pose_analysis import analyze_video
from scoring import score_movement
from training_plan import generate_training_plan

app = FastAPI(title="FootballIQ AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

init_db()


@app.get("/")
def root():
    return {"status": "FootballIQ AI backend is running"}


@app.post("/players")
def create_player(name: str = Form(...), age: int = Form(...), city: str = Form("")):
    db = get_session()
    player = Player(name=name, age=age, city=city)
    db.add(player)
    db.commit()
    db.refresh(player)
    return {"id": player.id, "name": player.name}


@app.post("/sessions")
async def upload_drill(
    player_id: int = Form(...),
    drill_type: str = Form(...),  # dribbling | passing | shooting | first_touch
    video: UploadFile = File(...),
):
    db = get_session()
    player = db.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Save uploaded video
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(video.file, f)

    # 1. Pose estimation -> movement data
    movement_data = analyze_video(filepath, drill_type)

    # 2. Scoring -> category scores + feedback
    result = score_movement(movement_data, drill_type)

    # 3. Persist session + scores
    drill_session = DrillSession(player_id=player_id, drill_type=drill_type, video_path=filepath)
    db.add(drill_session)
    db.commit()
    db.refresh(drill_session)

    for category, score in result["scores"].items():
        db.add(SkillScore(
            session_id=drill_session.id,
            player_id=player_id,
            drill_type=drill_type,
            category=category,
            score=score,
        ))
    db.commit()

    return {
        "session_id": drill_session.id,
        "drill_type": drill_type,
        "scores": result["scores"],
        "feedback": result["feedback"],
    }


@app.get("/players/{player_id}/history")
def get_history(player_id: int):
    db = get_session()
    scores = db.query(SkillScore).filter(SkillScore.player_id == player_id).all()
    return [
        {
            "session_id": s.session_id,
            "drill_type": s.drill_type,
            "category": s.category,
            "score": s.score,
        }
        for s in scores
    ]


@app.get("/players/{player_id}/plan")
def get_plan(player_id: int):
    db = get_session()
    scores = db.query(SkillScore).filter(SkillScore.player_id == player_id).all()
    if not scores:
        raise HTTPException(status_code=404, detail="No sessions yet for this player")
    plan = generate_training_plan(scores)
    return plan


# Serve frontend static files (for simple deployment)
if os.path.isdir("../frontend"):
    app.mount("/app", StaticFiles(directory="../frontend", html=True), name="frontend")
