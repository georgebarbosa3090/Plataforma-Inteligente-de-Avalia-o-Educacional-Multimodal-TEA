import requests
import time

URL = "http://127.0.0.1:8000"

def test():
    # 1. Criar Atividade
    try:
        act_res = requests.post(f"{URL}/activities/", json={
            "title": "Teste de Alerta Multimodal",
            "description": "Explique seu sentimento hoje."
        })
        act_id = act_res.json()["id"]
        print(f"Atividade criada ID: {act_id}")

        # 2. Simular Resposta Negativa (NLP)
        print("Enviando resposta negativa...")
        requests.post(f"{URL}/activities/{act_id}/respond/", json={
            "student_id": "Estudante_Teste",
            "content": "Estou muito frustrado, nada funciona e o curso é péssimo."
        })

        # 3. Simular Baixa Atenção (Vision)
        # Usando um frame preto para garantir atenção 0
        import base64
        import numpy as np
        import cv2
        dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
        _, buffer = cv2.imencode('.jpg', dummy_img)
        b64 = base64.b64encode(buffer).decode()
        
        print("Enviando frame de baixa atenção...")
        requests.post(f"{URL}/activities/{act_id}/vision/", json={
            "student_id": "Estudante_Teste",
            "image_base64": b64
        })

        # 4. Verificar Alertas
        time.sleep(1)
        alerts = requests.get(f"{URL}/activities/{act_id}/alerts/").json()
        print(f"Total de alertas gerados: {len(alerts)}")
        for a in alerts:
            print(f"- [{a['priority']}] {a['type']}: {a['message']}")

    except Exception as e:
        print(f"Erro no teste: {e}")

if __name__ == "__main__":
    test()
