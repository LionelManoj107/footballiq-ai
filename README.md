# FootballIQ AI ⚽🧠

I built FootballIQ AI as my submission for the Idea2Impact 2026 Hackathon, under the
**Sustainability & Social Impact** theme (Skill Development domain).

🔗 **Live Demo:** https://footballiq-ai.onrender.com
🎥 **Demo Video:** https://drive.google.com/file/d/1rUOD_XOmk0rOkEcs4DGaxesWkUZvn8lN/view?usp=sharing

---

## Why I Built This

Football participation in India is growing fast, especially with global events like the
FIFA World Cup pulling in new interest. But when I looked at who actually gets access to
real coaching, it's mostly players in big cities with established academies. A player in
a grassroots setup or a small-town school team has no realistic way to get objective
feedback on their technique, and no way to build a track record that a scout or academy
could look at remotely. That's the specific gap I wanted to build for.

## What It Does

FootballIQ AI lets a player record a short video of themselves doing a drill —
dribbling, passing, shooting, or first touch — and get back an AI-generated skill
assessment: category scores plus specific, actionable feedback (not generic tips). It
tracks scores over time and builds a personalized weekly training plan around whatever
skill is currently weakest.

## How I Built the AI Pipeline

1. **Video capture** — player uploads a drill clip through the frontend.
2. **Pose estimation** — I extract body position, foot placement, and ball-contact
   points from the video (currently using a working stub while I wire in MediaPipe for
   full pose estimation — see the note in `pose_analysis.py`).
3. **Skill scoring** — the extracted movement data is compared against benchmark
   technique for that specific drill to produce category scores (control, technique,
   balance, accuracy) with feedback text.
4. **Progress tracking** — every session gets logged per player.
5. **Training plan generation** — I turn the accumulated skill history into a weekly
   plan targeting the player's lowest-scoring category.

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, FastAPI |
| AI | Pose estimation (MediaPipe, in progress) + a scoring model + rule-based training-plan generation |
| Database | SQLite / PostgreSQL |
| Frontend | HTML/CSS/JS — kept lightweight since most players will use it on a phone |
| Deployment | Render |

## Project Structure

```
footballiq-ai/
├── backend/
│   ├── main.py                # FastAPI app entrypoint
│   ├── pose_analysis.py       # Video -> pose/movement extraction
│   ├── scoring.py             # Movement data -> skill scores + feedback
│   ├── training_plan.py       # Skill history -> personalized weekly plan
│   ├── models.py              # DB models (player, session, skill_score)
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── README.md
└── .env.example
```

## Running It Locally

```bash
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
# open index.html via a local server, or serve it through FastAPI's static files
```

## Environment Variables

```
LLM_API_KEY=your_key_here
DATABASE_URL=sqlite:///./footballiq.db
```

## Deploying (Render)

1. Push this repo to GitHub (must be public for judging).
2. On Render: **New → Web Service** → connect the repo.
3. Build command: `pip install -r backend/requirements.txt`
4. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add `LLM_API_KEY` under Environment variables.
6. Deploy — Render gives a public `.onrender.com` URL, which I use for the submission form.

## What's Next

The pose-estimation stage is currently a working placeholder so the full pipeline runs
end-to-end. The next iteration wires in real MediaPipe-based pose extraction (sketched
out in `pose_analysis.py`) for genuine computer-vision-based technique analysis.

## Submission

Individual submission — Idea2Impact 2026 Online Hackathon.

## License

MIT
