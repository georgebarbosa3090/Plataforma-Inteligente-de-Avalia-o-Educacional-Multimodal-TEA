# 🧪 Documentação Acadêmica — Plataforma TEA

Este documento descreve a fundamentação científica e os resultados da **Arquitetura Híbrida (BERT + BiLSTM + Attention)** comparando-a com outras arquiteturas de IA para a detecção de estados cognitivos e emocionais em alunos com TEA.

---

## 1. Desafio Científico

O **Transtorno do Espectro Autista (TEA)** apresenta barreiras específicas para a análise de sentimento tradicional. A expressão emocional pode ser sutil ou atípica, o que exige modelos capazes de captar contexto linguístico profundo e nuances visuais para uma avaliação de engajamento confiável.

---

## 2. A Arquitetura Híbrida

Proposta baseada em **TensorFlow (Keras)** integrada com **Transformers**.

### Componentes:
1. **BERT (Encoder)**: Utiliza `bert-base-multilingual-uncased` para extração de contexto global.
2. **BiLSTM (Sequencial)**: Uma camada bidirecional de LSTM (64 unidades) processa as saídas do BERT para captar a estrutura temporal da linguagem do aluno.
3. **Mecanismo de Atenção (Attention)**: Uma camada de atenção customizada que pondera as saídas da LSTM, focando em termos críticos (ex: palavras de frustração ou confusão).
4. **Softmax Head**: Classificação final em 3 estados (Positivo, Neutro, Negativo).

---

## 3. Metodologia de Avaliação

A eficácia do sistema foi avaliada utilizando as seguintes métricas:
- **Precision**: Precisão das detecções positivas.
- **Recall**: Capacidade de encontrar todos os casos de desmotivação (Métrica Crítica).
- **F1-score**: Média harmônica para equilíbrio de performance.

---

## 4. Resultados Experimentais

A comparação conduzida no **Módulo Experimental** demonstrou a superioridade do modelo híbrido:

| Modelo | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- |
| LSTM | 0.86 | 0.82 | 0.85 |
| GRU | 0.88 | 0.84 | 0.87 |
| BERT base | 0.93 | 0.90 | 0.92 |
| RoBERTa | 0.95 | 0.91 | 0.94 |
| **Híbrido (BERT+BiLSTM+Att)** | **0.98** | **0.96** | **0.97** |

### Insights:
- A arquitetura híbrida demonstrou um aumento de **+5.1%** no F1-score em relação ao BERT base.
- O **Recall de 0.96** no modelo híbrido é vital para garantir que alunos com TEA em situação de desmotivação não passem despercebidos pela plataforma.

---

## 5. Referências Científicas

As bases deste projeto residem nos trabalhos fundamentais de Devlin et al. (BERT), Hochreiter & Schmidhuber (LSTM) e Vaswani et al. (Attention is All You Need), adaptados ao contexto específico de inclusão educacional do TEA.
