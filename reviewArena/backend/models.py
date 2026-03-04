from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    reviews = relationship("Review", back_populates="model")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    model_id = Column(Integer, ForeignKey("models.id"))
    model = relationship("Model", back_populates="reviews")

class Comparison(Base):
    __tablename__ = "comparisons"
    id = Column(Integer, primary_key=True)
    review_a_id = Column(Integer, ForeignKey("reviews.id"))
    review_b_id = Column(Integer, ForeignKey("reviews.id"))

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.id"))
    winner_model_id = Column(Integer, ForeignKey("models.id"), nullable=True)