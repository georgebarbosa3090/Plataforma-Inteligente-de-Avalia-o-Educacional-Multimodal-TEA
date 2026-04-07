from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .database.models import Base, Activity, Response, VisionLog, Alert
from .services.nlp_service import nlp_analyzer
from .services.vision_service import vision_analyzer
from .services.fusion_service import fusion_manager
from .services.scientific_module import scientific_evaluator
from pydantic import BaseModel
from typing import List
import os

# Configuração do Banco de Dados SQLite
DATABASE_URL = "sqlite:///./tea_platform.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Inicializar Tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plataforma TEA — Backend API")

# Dependência Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class ActivityCreate(BaseModel):
    title: str
    description: str

class ResponseCreate(BaseModel):
    student_id: str
    content: str

class VisionFrame(BaseModel):
    student_id: str
    image_base64: str

# Endpoints
@app.get("/")
def read_root():
    return {"message": "Plataforma TEA backend rodando com sucesso."}

@app.post("/activities/", response_model=None)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = Activity(title=activity.title, description=activity.description)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@app.get("/activities/", response_model=None)
def list_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()

@app.post("/activities/{activity_id}/respond/", response_model=None)
def submit_response(activity_id: int, response: ResponseCreate, db: Session = Depends(get_db)):
    # 1. Verificar se a atividade existe
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # 2. Processar Sentimento via NLP
    analysis = nlp_analyzer.analyze_sentiment(response.content)

    # 3. Salvar no Banco
    db_response = Response(
        activity_id=activity_id,
        student_id=response.student_id,
        content=response.content,
        sentiment=analysis["sentiment"],
        sentiment_score=analysis["score"],
        engagement=analysis["engagement"]
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    # --- NOVO: Verificar Alertas ---
    fusion_manager.verify_and_generate_alerts(db, activity_id, response.student_id)
    
    return db_response

@app.post("/activities/{activity_id}/vision/", response_model=None)
def submit_vision_frame(activity_id: int, frame: VisionFrame, db: Session = Depends(get_db)):
    # 1. Processar Frame via Visão Computacional
    analysis = vision_analyzer.analyze_frame(frame.image_base64)
    
    if not analysis:
        raise HTTPException(status_code=400, detail="Erro ao processar imagem")

    # 2. Salvar Log de Visão
    db_vision = VisionLog(
        activity_id=activity_id,
        student_id=frame.student_id,
        attention_score=analysis["attention_score"],
        emotion=analysis["emotion"]
    )
    db.add(db_vision)
    db.commit()
    db.refresh(db_vision)
    
    # --- NOVO: Verificar Alertas ---
    fusion_manager.verify_and_generate_alerts(db, activity_id, frame.student_id)
    
    return db_vision

@app.get("/activities/{activity_id}/stats/", response_model=None)
def get_activity_stats(activity_id: int, db: Session = Depends(get_db)):
    responses = db.query(Response).filter(Response.activity_id == activity_id).all()
    vision_logs = db.query(VisionLog).filter(VisionLog.activity_id == activity_id).all()
    
    if not responses and not vision_logs:
        return {"total": 0, "sentiment_distribution": {}, "engagement_distribution": {}, "avg_attention": 0}

    sentiments = {}
    engagements = {}
    for r in responses:
        sentiments[r.sentiment] = sentiments.get(r.sentiment, 0) + 1
        engagements[r.engagement] = engagements.get(r.engagement, 0) + 1
        
    avg_attention = 0
    emotions = {}
    if vision_logs:
        avg_attention = sum(v.attention_score for v in vision_logs) / len(vision_logs)
        for v in vision_logs:
            emotions[v.emotion] = emotions.get(v.emotion, 0) + 1
        
    return {
        "total_responses": len(responses),
        "sentiment_distribution": sentiments,
        "engagement_distribution": engagements,
        "avg_attention": round(avg_attention, 2),
        "emotion_distribution": emotions,
        "raw_responses": responses
    }

@app.get("/activities/{activity_id}/alerts/", response_model=None)
def list_activity_alerts(activity_id: int, db: Session = Depends(get_db)):
    """
    Retorna os alertas críticos para uma atividade específica.
    """
    return db.query(Alert).filter(Alert.activity_id == activity_id).order_by(Alert.timestamp.desc()).all()

@app.get("/research/results/", response_model=None)
def get_research_results():
    """
    Retorna os resultados comparativos científicos (Módulo Experimental).
    """
    return scientific_evaluator.get_detailed_report()
