# 🏗️ Arquitetura Técnica — Plataforma TEA

Este documento detalha o funcionamento interno de baixo nível da **Plataforma TEA (Avaliação Multimodal)**, descrevendo o fluxo de dados, a stack tecnológica e a engenharia de modelos.

---

## 🗺️ Visão Geral do Sistema

A plataforma é baseada em uma arquitetura de microsserviços centralizada em um **Backend FastAPI**.

```mermaid
graph TD
    subgraph Frontend (Streamlit)
        A[Interface Aluno] --> |Webcam/Texto| B[Interação]
        C[Dashboard Professor] --> |Visualização| D[Insights/Alertas]
    end

    subgraph Backend (FastAPI)
        E[API Endpoints] --> |Request| F[NLP Service]
        E --> |Request| G[Vision Service]
        F --> |Score Texto| H[Fusion Service]
        G --> |Score Foco| H
        H --> |Gatilhos| I[Alert Engine]
    end

    subgraph Database
        J[(SQLite - models.py)]
    end

    E <--> J
    I --> J
```

---

## 🛠️ Detalhamento dos Módulos

### 1. Módulo de Visão (CV)
O `vision_service.py` utiliza o **MediaPipe Face Mesh**. Ele extrai 468 landmarks faciais em real-time a partir de frames Base64. A lógica de "Head Pose Detection" calcula a correlação entre o nariz e os cantos dos olhos para determinar se o aluno está focado na tela.

### 2. Módulo de NLP
O `nlp_service.py` utiliza inicialmente o BERT (Multilingual) para converter textos livres em vetores contextuais e classificar o sentimento em 3 estados (Positivo, Neutro, Negativo).

### 3. Fusion Service (Fusão Tardia)
O `fusion_service.py` realiza o processamento híbrido:
- **Index de Engajamento Híbrido (IEH)**: Fórmula ponderada $IEH = (Atenção \times 0.6) + (Sentimento \times 0.4)$.
- **Alert Engine**: Monitoramento de janelas temporais de dados para identificar quedas bruscas de performance (ex: 3 eventos seguidos de baixa atenção).

---

## 🗄️ Esquema do Banco de Dados

Utilizamos SQLAlchemy com SQLite para persistência:
- **activities**: Cadastro de questões e títulos.
- **responses**: Texto, sentimento (NLP) e engajamento textual.
- **vision_logs**: Score de atenção e emoção facial (CV).
- **alerts**: Histórico de notificações críticas enviadas ao professor.

---

## 🔗 Fluxo Multimodal (Data Path)

1. O **Aluno** responde uma atividade discursiva.
2. Simultaneamente, a **Webcam** captura um frame de atenção.
3. O **Backend** recebe os dados e orquestra o processamento paralelo (NLP e CV).
4. O **Fusion Service** consolida os resultados.
5. Se o score híbrido for crítico, o **Alert Engine** dispara uma notificação.
6. O **Professor** visualiza o alerta e os gráficos detalhados no Dashboard.
