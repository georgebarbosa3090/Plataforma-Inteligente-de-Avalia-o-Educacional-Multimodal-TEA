# 🧠 Plataforma Inteligente de Avaliação Multimodal (TEA)

Esta plataforma é uma solução completa de hardware e software para análise de engajamento e sentimento em ambientes educacionais, com foco especializado em alunos com **Transtorno do Espectro Autista (TEA)**. O sistema utiliza a integração de **Processamento de Linguagem Natural (NLP)** e **Visão Computacional (CV)** para fornecer insights proativos e científicos sobre o estado emocional e cognitivo dos estudantes.

---

## 🚀 Principais Funcionalidades

### 📈 Análise Multimodal
Integração de dados de texto (respostas discursivas) e imagem (atenção facial via webcam) para uma avaliação 360º de engajamento.

### 🔔 Alertas Inteligentes
Sistema automático de notificações para professores em casos de:
- Baixa atenção visual sustentada.
- Sentimentos negativos ou frustração detectados no texto ou face.
- Quedas bruscas no índice de engajamento híbrido.

### 🧪 Módulo Experimental Científico
A plataforma inclui um laboratório de testes que compara diferentes arquiteturas de Deep Learning (LSTM, GRU, BERT, RoBERTa) com o modelo híbrido **BERT + BiLSTM + Attention**.

---

## 🛠️ Stack Tecnológica

- **Backend**: Python (FastAPI), SQLAlchemy (SQLite).
- **IA/ML**: TensorFlow, HuggingFace Transformers (BERT), MediaPipe.
- **Frontend**: Streamlit.
- **Métricas**: Scikit-Learn.

---

## 📦 Guia de Instalação e Execução

### 1. Pré-requisitos
Certifique-se de ter o Python 3.9+ instalado em seu ambiente Windows/Linux/macOS.

### 2. Configurar o Ambiente
```powershell
# Criar diretório do projeto e instalar dependências
pip install -r tea-platform/requirements.txt
```

### 3. Rodar o Backend
O backend gerencia as APIs, o bando de dados e o processamento de IA.
```powershell
cd tea-platform
$env:PYTHONPATH = "."
uvicorn backend.main:app --reload --port 8000
```

### 4. Rodar o Frontend
A interface interativa para alunos e professores.
```powershell
streamlit run frontend/app.py
```

---

## 👥 Papéis do Sistema

- **👨‍🏫 Professor**: Cria atividades, monitora métricas globais da turma, recebe alertas e acessa o laboratório científico.
- **🎓 Aluno**: Responde atividades e ativa opcionalmente o monitor de atenção por webcam para suporte via IA.

---

## ⚖️ Ética e Privacidade (LGPD)
- Frames de vídeo são processados em memória e **anonimizados imediatamente**.
- O sistema não armazena fotos ou vídeos dos alunos no banco de dados, apenas métricas matemáticas e logs de visão.

---

## 📜 Licença e Créditos
Desenvolvido por **Agente Antigravity** sob diretrizes científicas especializadas. 
A arquitetura híbrida foca na inclusão e melhoria do ambiente educacional para indivíduos neurodiversos.
