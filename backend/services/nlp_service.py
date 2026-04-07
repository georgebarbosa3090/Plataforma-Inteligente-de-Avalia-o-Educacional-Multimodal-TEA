from transformers import pipeline

class NLPService:
    def __init__(self):
        # Usando um modelo multilingue que suporta PT-BR por padrão
        # Este modelo classifica de 1 a 5 estrelas.
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis", 
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )

    def analyze_sentiment(self, text: str):
        """
        Analisa o sentimento do texto e mapeia para categorias simples.
        """
        try:
            result = self.sentiment_pipeline(text)[0]
            label = result['label'] # Ex: '1 star', '5 stars'
            score = result['score']
            
            # Mapeamento do modelo nlptown (1-5 estrelas) para Positivo/Neutro/Negativo
            stars = int(label.split()[0])
            
            if stars <= 2:
                sentiment = "Negativo"
            elif stars == 3:
                sentiment = "Neutro"
            else:
                sentiment = "Positivo"
                
            # Heurística simples de engajamento para o MVP
            # Baseado em tamanho do texto e confiança
            engagement_score = len(text.split())
            if engagement_score > 20:
                engagement = "Alto"
            elif engagement_score > 5:
                engagement = "Médio"
            else:
                engagement = "Baixo"

            return {
                "sentiment": sentiment,
                "score": score,
                "engagement": engagement
            }
        except Exception as e:
            print(f"Erro no processamento NLP: {e}")
            return {
                "sentiment": "Neutro",
                "score": 0.0,
                "engagement": "Baixo"
            }

# Singleton para evitar recarregar o modelo a cada request
nlp_analyzer = NLPService()
