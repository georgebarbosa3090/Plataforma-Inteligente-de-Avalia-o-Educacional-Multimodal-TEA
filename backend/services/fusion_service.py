from sqlalchemy.orm import Session
from ..database.models import Response, VisionLog, Alert

class FusionService:
    def calculate_hybrid_engagement(self, nlp_score: float, attention_score: float):
        """
        Combina o score de NLP (sentimento) e Visão (atenção) 
        para um índice de engajamento híbrido (0 a 100).
        """
        # Pesos sugeridos: 60% Visão (Foco), 40% Texto (Conteúdo)
        weight_vision = 0.6
        weight_nlp = 0.4
        
        # O score de sentimento do modelo nlptown é de 1-5 estrelas.
        # Mas o nlp_service já devolveu sentiment_score (confiança).
        # Vamos usar o score normalizado.
        
        hybrid_score = (attention_score * weight_vision) + (nlp_score * weight_nlp)
        return round(hybrid_score * 100, 2)

    def verify_and_generate_alerts(self, db: Session, activity_id: int, student_id: str):
        """
        Analisa os logs recentes e gera alertas se necessário.
        """
        # 1. Pegar logs recentes de Visão
        vision_logs = db.query(VisionLog).filter(
            VisionLog.activity_id == activity_id,
            VisionLog.student_id == student_id
        ).order_by(VisionLog.timestamp.desc()).limit(3).all()
        
        # 2. Pegar resposta recente de NLP
        last_response = db.query(Response).filter(
            Response.activity_id == activity_id,
            Response.student_id == student_id
        ).order_by(Response.timestamp.desc()).first()

        # --- Lógica de Gatilho ---
        alerts_created = []

        # Gatilho A: Baixa Atenção Visual Recorrente
        if vision_logs and all(v.attention_score < 0.4 for v in vision_logs):
            msg = f"O aluno {student_id} apresentou baixa atenção visual recorrente nos últimos 3 registros."
            alert = self._create_alert(db, activity_id, student_id, "Baixa Atenção", "Alta", msg)
            alerts_created.append(alert)

        # Gatilho B: Sentimento Negativo Detectado no Texto
        if last_response and last_response.sentiment == "Negativo":
            msg = f"O conteúdo textual do aluno {student_id} indica frustração ou sentimento negativo."
            alert = self._create_alert(db, activity_id, student_id, "Desmotivação", "Média", msg)
            alerts_created.append(alert)

        # Gatilho C: Emoção Visual de Frustração
        if vision_logs and any(v.emotion == "Surpresa/Frustração" for v in vision_logs):
            msg = f"Detectada expressão facial de frustração no aluno {student_id}."
            alert = self._create_alert(db, activity_id, student_id, "Estado Emocional", "Média", msg)
            alerts_created.append(alert)

        return alerts_created

    def _create_alert(self, db: Session, activity_id: int, student_id: str, type: str, priority: str, message: str):
        # Evitar duplicados idênticos em curto período (opcional no MVP)
        new_alert = Alert(
            activity_id=activity_id,
            student_id=student_id,
            type=type,
            priority=priority,
            message=message
        )
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        return new_alert

fusion_manager = FusionService()
