import streamlit as st
import requests
import pandas as pd
import json
import base64

# Configuração da Página
st.set_page_config(page_title="Plataforma TEA — MVP", layout="wide")

# URL do Backend (ajuste conforme necessário)
BACKEND_URL = "http://localhost:8000"

st.title("🧠 Plataforma TEA — Avaliação Multimodal")
st.markdown("---")

# Navegação Lateral
role = st.sidebar.selectbox("Escolha seu papel:", ["👨‍🏫 Professor", "🎓 Aluno"])

if role == "👨‍🏫 Professor":
    st.header("Dashboard do Professor")
    
    tabs = st.tabs(["📊 Visão Geral", "🔔 Alertas", "🧪 Módulo Experimental", "➕ Criar Atividade", "📥 Respostas Detalhadas"])
    
    with tabs[3]:
        st.subheader("Criar Nova Atividade")
        title = st.text_input("Título da Atividade")
        desc = st.text_area("Descrição / Questão Discursiva")
        if st.button("Publicar Atividade"):
            payload = {"title": title, "description": desc}
            r = requests.post(f"{BACKEND_URL}/activities/", json=payload)
            if r.status_code == 200:
                st.success("Atividade criada com sucesso!")
            else:
                st.error("Erro ao criar atividade. Verifique se o backend está rodando.")

    with tabs[0]:
        st.subheader("Análise de Engajamento e Sentimento")
        # Listagem para selecionar atividade
        try:
            r_list = requests.get(f"{BACKEND_URL}/activities/")
            if r_list.status_code == 200:
                activities = r_list.json()
                if not activities:
                    st.info("Nenhuma atividade criada ainda.")
                else:
                    activity_names = {a['title']: a['id'] for a in activities}
                    selected_name = st.selectbox("Selecione a atividade para análise:", list(activity_names.keys()))
                    
                    # Carregar estatísticas
                    r_stats = requests.get(f"{BACKEND_URL}/activities/{activity_names[selected_name]}/stats/")
                    if r_stats.status_code == 200:
                        stats = r_stats.json()
                        
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Respostas Bancadas", stats['total_responses'])
                        col2.metric("Atenção Média", f"{int(stats['avg_attention']*100)}%")
                        
                        if stats['total_responses'] > 0 or stats.get('emotion_distribution'):
                            # Gráficos
                            with col3:
                                st.write("**Sentimento (Texto)**")
                                st.bar_chart(stats['sentiment_distribution'])
                            with col4:
                                st.write("**Emoções (Visual)**")
                                st.bar_chart(stats['emotion_distribution'])
                        else:
                            st.warning("Aguardando os primeiros dados dos alunos...")
            else:
                st.error("Falha ao comunicar com o backend.")
        except Exception as e:
            st.error(f"Backend Offline: {e}")

    with tabs[1]:
        st.subheader("🔔 Alertas de Atenção e Engajamento")
        try:
            r_list = requests.get(f"{BACKEND_URL}/activities/")
            if r_list.status_code == 200 and r_list.json():
                activities = r_list.json()
                activity_names = {a['title']: a['id'] for a in activities}
                selected_a_alerts = st.selectbox("Ver alertas de:", list(activity_names.keys()), key="alert_sel")
                
                r_alerts = requests.get(f"{BACKEND_URL}/activities/{activity_names[selected_a_alerts]}/alerts/")
                if r_alerts.status_code == 200:
                    alerts = r_alerts.json()
                    if not alerts:
                        st.success("Nenhum alerta crítico para esta atividade. Bom trabalho!")
                    else:
                        for alert in alerts:
                            color = "red" if alert['priority'] == "Alta" else "orange"
                            st.error(f"**[{alert['type']}]** ({alert['priority']}): {alert['message']}  \n*Estudante: {alert['student_id']}*")
        except:
            st.error("Erro ao carregar alertas.")

    with tabs[2]:
        st.subheader("🧪 Módulo Experimental (Pesquisa Científica)")
        st.write("Comparação de performance entre arquiteturas de Deep Learning para detecção de desmotivação (Dataset TEA).")
        
        try:
            r_research = requests.get(f"{BACKEND_URL}/research/results/")
            if r_research.status_code == 200:
                res = r_research.json()
                
                # Tabela de Comparação
                st.markdown("### 📈 Tabela Comparativa de Modelos")
                comp_df = pd.DataFrame(res['comparison']).T
                st.table(comp_df.style.highlight_max(axis=0, color='lightgreen'))
                
                # Insights Científicos
                col_a, col_b = st.columns(2)
                with col_a:
                    st.success(f"**Melhor Modelo**: {res['best_model']}")
                    st.info(f"**Melhoria**: {res['f1_improvement']}")
                
                with col_b:
                    st.markdown("### 🧩 Matriz de Confusão (Híbrido)")
                    # Visualização simples da matriz
                    matrix = res['confusion_matrix']
                    st.write("Verdadeiro \ Predito")
                    st.dataframe(pd.DataFrame(matrix, index=['Neg', 'Neu', 'Pos'], columns=['Neg', 'Neu', 'Pos']))
                
        except:
            st.error("Erro ao carregar dados científicos.")

    with tabs[4]:
        st.subheader("Log de Respostas Analisadas")
        # Mostrar tabela bruta
        try:
            r_list = requests.get(f"{BACKEND_URL}/activities/")
            if r_list.status_code == 200 and r_list.json():
                activities = r_list.json()
                activity_names = {a['title']: a['id'] for a in activities}
                selected_name_log = st.selectbox("Ver log de:", list(activity_names.keys()), key="log_sel")
                
                r_log = requests.get(f"{BACKEND_URL}/activities/{activity_names[selected_name_log]}/stats/")
                if r_log.status_code == 200:
                    raw_data = r_log.json().get('raw_responses', [])
                    if raw_data:
                        df = pd.DataFrame(raw_data)
                        st.dataframe(df[['student_id', 'content', 'sentiment', 'engagement', 'sentiment_score']])
                    else:
                        st.write("Sem registros.")
        except:
            pass

elif role == "🎓 Aluno":
    st.header("Área do Aluno")
    
    try:
        r_list = requests.get(f"{BACKEND_URL}/activities/")
        if r_list.status_code == 200:
            activities = r_list.json()
            if not activities:
                st.info("Nenhuma atividade disponível no momento. Aguarde o professor.")
            else:
                activity_names = {a['title']: a['id'] for a in activities}
                selected_activity = st.selectbox("Selecione a atividade:", list(activity_names.keys()))
                
                # Detalhes da atividade
                selected_id = activity_names[selected_activity]
                activity_data = next(item for item in activities if item["id"] == selected_id)
                
                st.info(f"**Instrução:** {activity_data['description']}")
                
                student_id = st.text_input("Seu Nome/ID")
                
                # --- NOVO: Módulo de Visão ---
                st.subheader("📷 Monitor de Atenção (Opcional)")
                enable_vision = st.checkbox("Ativar câmera para análise de foco (IA)")
                
                if enable_vision:
                    img_file = st.camera_input("Capture um frame para análise de atenção")
                    if img_file:
                        # Converter para Base64
                        bytes_data = img_file.getvalue()
                        base64_image = base64.b64encode(bytes_data).decode('utf-8')
                        
                        # Enviar para o Backend
                        if st.button("Enviar Análise de Foco"):
                            v_payload = {"student_id": student_id, "image_base64": base64_image}
                            v_res = requests.post(f"{BACKEND_URL}/activities/{selected_id}/vision/", json=v_payload)
                            if v_res.status_code == 200:
                                st.success("Análise de atenção enviada!")
                            else:
                                st.error("Erro ao enviar imagem.")

                st.subheader("📝 Sua Resposta")
                answer = st.text_area("Escreva aqui:", height=200)
                
                if st.button("Enviar Resposta"):
                    if not student_id or not answer:
                        st.warning("Preencha todos os campos!")
                    else:
                        payload = {"student_id": student_id, "content": answer}
                        r_post = requests.post(f"{BACKEND_URL}/activities/{selected_id}/respond/", json=payload)
                        if r_post.status_code == 200:
                            st.success("Resposta enviada! A IA está processando seu engajamento.")
                            st.balloons()
                        else:
                            st.error("Falha no envio.")
        else:
            st.error("Conexão com o backend falhou.")
    except Exception as e:
        st.error(f"Erro: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Antigravity Framework v1.0 — MVP Phase 1")
