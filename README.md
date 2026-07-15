bash

cat /home/claude/khelsetu/README.md
Output

# FootballIQ AI ⚽🧠

**AI-powered skill assessment and training coach for grassroots football players in India.**
Built for Idea2Impact 2026 Hackathon — Theme: *Sustainability & Social Impact (Skill Development)*

🔗 **Live Demo:** [add your Render URL here]
🎥 **Demo Video:** [add your YouTube/Drive link here]

---

## The Problem

Football participation in India is surging, driven in part by global events like the FIFA
World Cup — but grassroots and school-level players outside major cities have almost no
access to structured coaching or objective skill feedback. Talented players go unnoticed
because there's no low-cost, consistent way to measure their technique or build a track
record visible to academies and scouts.

## The Solution

FootballIQ AI lets a player record a short video of a football drill (dribbling, passing,
shooting, first touch) and get an AI-generated skill assessment with specific feedback,
tracked over time, plus a personalized weekly training plan targeting their weakest skill.
A shareable Player Profile gives players outside traditional networks visibility to
coaches and scouts.

## How It Works (AI Pipeline)

1. **Video capture** — player uploads a short clip of a specific drill.
2. **Pose estimation / computer vision** — extracts body position, foot placement, and
   ball-contact points from the video.
3. **Skill scoring** — compares extracted movement against benchmark technique for that
   drill, producing category scores (control, technique, balance, accuracy) + specific
   feedback text.
4. **Progress tracking** — scores logged per player over time.
5. **Personalized training plan** — generated weekly, targeting the player's lowest-scoring
   skill area.

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, FastAPI |
| AI | Pose estimation (e.g. MediaPipe/OpenPose) + scoring model + LLM for feedback/plan generation |
| Database | SQLite / PostgreSQL (player profile, skill history) |
| Frontend | HTML/CSS/JS (mobile-first — most players will use a phone) |
| Deployment | Render |

## Project Structure

```
footballiq-ai/
├── backend/
│   ├── main.py                # FastAPI app entrypoint
│   ├── pose_analysis.py       # Video → pose/movement extraction
│   ├── scoring.py             # Movement data → skill scores + feedback
│   ├── training_plan.py       # Skill history → personalized weekly plan
│   ├── models.py              # DB models (player, session, skill_score)
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── README.md
└── .env.example
```

## Setup Instructions

```bash
# clone
git clone https://github.com/<your-username>/footballiq-ai.git
cd footballiq-ai

# backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your LLM API key
uvicorn main:app --reload

# frontend
cd ../frontend
# open index.html via a local server, or serve via FastAPI static files
```

## Environment Variables

```
LLM_API_KEY=your_key_here
DATABASE_URL=sqlite:///./footballiq.db
```

## Deployment (Render)

1. Push this repo to GitHub (public).
2. On Render: **New → Web Service** → connect the repo.
3. Build command: `pip install -r backend/requirements.txt`
4. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add `LLM_API_KEY` under Environment variables.
6. Deploy — Render gives you a public `.onrender.com` URL. Put that link in the submission form.

## Team

Individual submission — Idea2Impact 2026 Online Hackathon.

## License

MIT
Done
