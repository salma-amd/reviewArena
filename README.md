#ReviewArena

A minimal full-stack blind review comparison system where users vote on AI-generated academic paper reviews — without knowing which AI model wrote them.

#Overview

- Two reviews of two different hidden models are shown side by side (blind comparison)
- User votes for A, B, or Tie
- After voting, the model names are revealed
- A leaderboard ranks models by votes

#Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Database | SQLite + SQLAlchemy |
| Frontend | HTML + CSS + Vanilla JS |

---

#Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/salma-amd/reviewArena.git
cd reviewArena
```

### 2. Install dependencies
```bash
cd backend
pip install fastapi uvicorn sqlalchemy
```

### 3. Seed the database
```bash
python seed.py
```

### 4. Run the backend
```bash
uvicorn main:app --reload
```

### 5. Open the frontend
Open `frontend/index.html` in your browser.

---

#API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/comparison` | Returns a random blind comparison (no model names) |
| POST | `/vote` | Submits a vote (A, B, or tie) |
| GET | `/leaderboard` | Returns models ranked by votes |

---

#Project Structure

```
reviewArena/
├── backend/
│   ├── main.py        # API endpoints
│   ├── models.py      # Database models
│   ├── database.py    # Database connection
│   └── seed.py        # Seed script
└── frontend/
    └── index.html     # Full frontend (comparison + leaderboard)
```

---

#Notes

- Reviews are pre-seeded in the database (no AI integration required)
- No authentication or user management
- Built as a 1-2 hour prototype test
