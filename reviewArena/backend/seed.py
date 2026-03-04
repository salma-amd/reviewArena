from database import engine, SessionLocal, Base
from models import Model, Review, Comparison

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 1. Create 3 fake AI models
gpt = Model(name="GPT-5")
gemini = Model(name="Gemini-3 Pro")
claude = Model(name="Claude-4")

db.add_all([gpt, gemini, claude])
db.commit()

# 2. Create fake reviews 
reviews = [
    Review(text="This paper presents a strong methodology with clear experiments and reproducible results. The contribution to the field is significant.", model_id=gpt.id),
    Review(text="The methodology is unclear and the experiments lack proper baselines. The authors need to improve their literature review significantly.", model_id=gemini.id),
    Review(text="A well-structured paper with innovative ideas. However, the evaluation section could be more thorough and the writing needs polish.", model_id=claude.id),
]

db.add_all(reviews)
db.commit()

# 3. Create comparisons (pair reviews against each other)
comparisons = [
    Comparison(review_a_id=reviews[0].id, review_b_id=reviews[1].id),  # GPT vs Gemini
    Comparison(review_a_id=reviews[1].id, review_b_id=reviews[2].id),  # Gemini vs Claude
    Comparison(review_a_id=reviews[0].id, review_b_id=reviews[2].id),  # GPT vs Claude
]

db.add_all(comparisons)
db.commit()

db.close()
print("Database seeded successfully!")