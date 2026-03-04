from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import random

from database import engine, get_db, Base
from models import Model, Review, Comparison, Vote

app = FastAPI()

# This allows frontend HTML file to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# GET /comparison
# ─────────────────────────────────────────
@app.get("/comparison")
def get_comparison(db: Session = Depends(get_db)):
    comparisons = db.query(Comparison).all()
    if not comparisons:
        raise HTTPException(status_code=404, detail="No comparisons found")
    
    comparison = random.choice(comparisons)
    review_a = db.query(Review).filter(Review.id == comparison.review_a_id).first()
    review_b = db.query(Review).filter(Review.id == comparison.review_b_id).first()

    return {
        "comparison_id": comparison.id,
        "review_a": review_a.text,
        "review_b": review_b.text
    }

# ─────────────────────────────────────────
# POST /vote
# ─────────────────────────────────────────
class VoteRequest(BaseModel):
    comparison_id: int
    winner: str  # "A", "B", or "tie"

@app.post("/vote")
def post_vote(vote_req: VoteRequest, db: Session = Depends(get_db)):
    comparison = db.query(Comparison).filter(Comparison.id == vote_req.comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    review_a = db.query(Review).filter(Review.id == comparison.review_a_id).first()
    review_b = db.query(Review).filter(Review.id == comparison.review_b_id).first()

    # Decide which model won
    if vote_req.winner == "A":
        winner_model_id = review_a.model_id
    elif vote_req.winner == "B":
        winner_model_id = review_b.model_id
    else:  # tie
        winner_model_id = None

    # Save the vote
    vote = Vote(comparison_id=vote_req.comparison_id, winner_model_id=winner_model_id)
    db.add(vote)
    db.commit()

    # Return model names + updated vote counts
    models = db.query(Model).all()
    result = []
    for model in models:
        vote_count = db.query(Vote).filter(Vote.winner_model_id == model.id).count()
        result.append({"model": model.name, "votes": vote_count})

    # Also reveal which model was A and B
    model_a = db.query(Model).filter(Model.id == review_a.model_id).first()
    model_b = db.query(Model).filter(Model.id == review_b.model_id).first()

    return {
        "model_a": model_a.name,
        "model_b": model_b.name,
        "leaderboard": sorted(result, key=lambda x: x["votes"], reverse=True)
    }

# ─────────────────────────────────────────
# GET /leaderboard
# ─────────────────────────────────────────
@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    result = []
    for model in models:
        vote_count = db.query(Vote).filter(Vote.winner_model_id == model.id).count()
        result.append({"model": model.name, "votes": vote_count})

    return sorted(result, key=lambda x: x["votes"], reverse=True)