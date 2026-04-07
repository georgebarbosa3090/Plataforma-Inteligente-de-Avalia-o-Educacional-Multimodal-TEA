from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    student_id = Column(String)
    content = Column(String)
    sentiment = Column(String)  # Positivo, Neutro, Negativo
    sentiment_score = Column(Float)
    engagement = Column(String) # Alto, Médio, Baixo
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class VisionLog(Base):
    __tablename__ = "vision_logs"
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    student_id = Column(String)
    attention_score = Column(Float) # 0.0 a 1.0 (Focado)
    emotion = Column(String) # Alegria, Frustração, Atenção
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    student_id = Column(String)
    type = Column(String) # Baixa Atenção, Desmotivação, Frustração
    priority = Column(String) # Alta, Média, Baixa
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
